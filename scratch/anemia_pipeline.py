import cv2
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import os

# ---------------------------------------------------------
# PHASE 2.3 & 2.4: Setup Fuzzy Logic Controller
# ---------------------------------------------------------
def setup_fuzzy_controller():
    # Antecedent: Average Lightness (L channel from LAB) [0 to 255]
    l_mean = ctrl.Antecedent(np.arange(0, 256, 1), 'l_mean')
    
    # Consequent: Correction Factor [0.5 to 2.0]
    correction = ctrl.Consequent(np.arange(0.5, 2.1, 0.05), 'correction')

    # Membership functions for Lightness
    l_mean['dark'] = fuzz.trimf(l_mean.universe, [0, 0, 85])
    l_mean['dim'] = fuzz.trimf(l_mean.universe, [60, 100, 128])
    l_mean['normal'] = fuzz.trimf(l_mean.universe, [100, 130, 160])
    l_mean['bright'] = fuzz.trimf(l_mean.universe, [140, 180, 210])
    l_mean['overexposed'] = fuzz.trimf(l_mean.universe, [190, 255, 255])

    # Membership functions for Correction Factor
    correction['high_increase'] = fuzz.trimf(correction.universe, [1.4, 1.8, 2.0])
    correction['increase'] = fuzz.trimf(correction.universe, [1.1, 1.3, 1.5])
    correction['neutral'] = fuzz.trimf(correction.universe, [0.9, 1.0, 1.1])
    correction['decrease'] = fuzz.trimf(correction.universe, [0.7, 0.85, 1.0])
    correction['high_decrease'] = fuzz.trimf(correction.universe, [0.5, 0.6, 0.75])

    # Define Rules
    rule1 = ctrl.Rule(l_mean['dark'], correction['high_increase'])
    rule2 = ctrl.Rule(l_mean['dim'], correction['increase'])
    rule3 = ctrl.Rule(l_mean['normal'], correction['neutral'])
    rule4 = ctrl.Rule(l_mean['bright'], correction['decrease'])
    rule5 = ctrl.Rule(l_mean['overexposed'], correction['high_decrease'])

    correction_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5])
    return ctrl.ControlSystemSimulation(correction_ctrl)

fuzzy_sim = setup_fuzzy_controller()

# ---------------------------------------------------------
# PHASE 2.1: ROI Extraction Pipeline (OpenCV Haar Cascade)
# Uses 2-stage detection: Face → Eye → Lower eyelid crop
# More compatible than MediaPipe v1.0+ for Python 3.14
# ---------------------------------------------------------
def extract_conjunctiva_roi(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    h_img, w_img = image.shape[:2]

    # Load haarcascade XMLs from local folder (OpenCV 5 no longer bundles them)
    script_dir   = os.path.dirname(os.path.abspath(__file__))
    face_xml = os.path.join(script_dir, 'haarcascade_frontalface_default.xml')
    eye_xml  = os.path.join(script_dir, 'haarcascade_eye.xml')

    if not os.path.exists(face_xml) or not os.path.exists(eye_xml):
        print("  [Error] Haarcascade XML files not found in script folder.")
        print(f"  Expected location: {script_dir}")
        print("  Run: Invoke-WebRequest -Uri https://raw.githubusercontent.com/opencv/opencv/master/data/haarcascades/haarcascade_frontalface_default.xml -OutFile haarcascade_frontalface_default.xml")
        return image

    # Stage 1: Detect face first to narrow search region
    face_cascade = cv2.CascadeClassifier(face_xml)
    eye_cascade  = cv2.CascadeClassifier(eye_xml)

    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(80, 80))

    if len(faces) == 0:
        print("  [Warning] No face detected. Using lower-center crop as fallback.")
        # Fallback: crop bottom-half centre — where the conjunctiva sits in macro shots
        return image[int(h_img * 0.50):int(h_img * 0.95), int(w_img * 0.15):int(w_img * 0.85)]

    # Pick the largest detected face
    faces = sorted(faces, key=lambda r: r[2] * r[3], reverse=True)
    fx, fy, fw, fh = faces[0]
    face_roi_gray  = gray[fy:fy+fh, fx:fx+fw]
    face_roi_color = image[fy:fy+fh, fx:fx+fw]

    # Stage 2: Detect eyes within the face region
    eyes = eye_cascade.detectMultiScale(face_roi_gray, scaleFactor=1.05, minNeighbors=5, minSize=(20, 20))

    if len(eyes) == 0:
        print("  [Warning] No eye detected within face. Using lower-face crop as fallback.")
        # Use lower half of face (where eyes/conjunctiva typically sit)
        return face_roi_color[int(fh * 0.50):int(fh * 0.95), int(fw * 0.15):int(fw * 0.85)]

    # Pick the most prominent eye (largest area)
    eyes = sorted(eyes, key=lambda r: r[2] * r[3], reverse=True)
    ex, ey, ew, eh = eyes[0]

    # Stage 3: Crop the LOWER portion of the eye box → the conjunctiva / lower eyelid
    # The lower eyelid (pink tissue) sits in the bottom 40% of the eye bounding box
    # Add vertical padding below to capture the pulled-down tissue
    pad_top    = int(eh * 0.5)   # start halfway down the eye box
    pad_bottom = int(eh * 0.8)   # generous downward padding
    pad_left   = int(ew * 0.1)
    pad_right  = int(ew * 0.1)

    x1 = max(0, ex - pad_left)
    x2 = min(fw, ex + ew + pad_right)
    y1 = max(0, ey + pad_top)
    y2 = min(fh, ey + eh + pad_bottom)

    roi = face_roi_color[y1:y2, x1:x2]

    if roi.size == 0:
        print("  [Warning] ROI crop empty. Returning full face region.")
        return face_roi_color

    print(f"  [ROI] Conjunctiva region extracted: {roi.shape[1]}x{roi.shape[0]} px")
    return roi


# ---------------------------------------------------------
# PHASE 2.2 - 2.6: Fuzzy Logic Color Correction
# ---------------------------------------------------------
def apply_fuzzy_correction(roi_bgr):
    """
    Phase 2: Illumination-normalized color correction.
    Uses fuzzy membership to derive adaptive gamma, followed by CLAHE
    to preserve vascular microtexture and prevent highlight clipping.
    """
    # Convert RGB -> LAB
    lab = cv2.cvtColor(roi_bgr, cv2.COLOR_BGR2LAB)
    l_channel, a_channel, b_channel = cv2.split(lab)
    
    # Get average lightness
    avg_l = np.mean(l_channel)
    
    # Input to fuzzy logic
    fuzzy_sim.input['l_mean'] = avg_l
    fuzzy_sim.compute()
    
    # Get output correction factor
    factor = float(fuzzy_sim.output['correction'])
    
    # 1. Non-linear Gamma adjustment (preserves dynamic range without harsh clipping)
    gamma = 1.0 / max(factor, 0.2)
    table = np.array([((i / 255.0) ** gamma) * 255 for i in np.arange(0, 256)]).astype("uint8")
    gamma_l = cv2.LUT(l_channel, table)
    
    # 2. CLAHE (Contrast-Limited Adaptive Histogram Equalization)
    # Enhances micro-vascular capillary contrast while preventing overexposure
    clahe = cv2.createCLAHE(clipLimit=1.8, tileGridSize=(8, 8))
    corrected_l = clahe.apply(gamma_l)
    
    # Merge and convert back to BGR (a* and b* channels preserved intact)
    corrected_lab = cv2.merge((corrected_l, a_channel, b_channel))
    corrected_bgr = cv2.cvtColor(corrected_lab, cv2.COLOR_LAB2BGR)
    
    return corrected_bgr
# ---------------------------------------------------------
# PHASE 2.7: Erythema (Redness) Index Computation
# ---------------------------------------------------------
def calculate_erythema_index(roi_bgr):
    # EI = log(Red) - log(Green)
    # Add a small epsilon to prevent log(0)
    epsilon = 1e-5
    b, g, r = cv2.split(roi_bgr.astype(np.float32))
    
    ei = np.log10(r + epsilon) - np.log10(g + epsilon)
    avg_ei = np.mean(ei)
    return avg_ei

# ---------------------------------------------------------
# INPUT MODALITY: Camera vs Upload
# ---------------------------------------------------------
def get_user_input():
    print("========================================")
    print("Hemoglobin Estimation Input Selection")
    print("1. Capture via Webcam")
    print("2. Upload Image File (e.g., Kaggle Dataset)")
    print("========================================")
    
    choice = input("Enter choice (1 or 2): ").strip()
    
    if choice == '1':
        print("Opening Camera... Press SPACE to capture, Q to quit.")
        cap = cv2.VideoCapture(0)
        captured_frame = None
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            # Draw a guiding rectangle for the eye
            h, w = frame.shape[:2]
            cv2.rectangle(frame, (w//2 - 100, h//2 - 50), (w//2 + 100, h//2 + 50), (0, 255, 0), 2)
            cv2.putText(frame, "Align Eye Here - Press SPACE", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            
            cv2.imshow("Camera Feed", frame)
            key = cv2.waitKey(1) & 0xFF
            if key == 32:  # SPACE bar
                captured_frame = frame.copy()
                break
            elif key == ord('q'):
                break
                
        cap.release()
        cv2.destroyAllWindows()
        return captured_frame
        
    elif choice == '2':
        filepath = input("Enter the full absolute path to the image: ").strip()
        # Strip surrounding quotes that Windows adds when dragging/copying paths
        filepath = filepath.strip('"').strip("'")
        print(f"  -> Resolved path: {filepath}")
        if not os.path.exists(filepath):
            print(f"Error: File not found at resolved path above. Check the path carefully.")
            return None
        return cv2.imread(filepath)
    else:
        print("Invalid choice.")
        return None

# ---------------------------------------------------------
# MAIN PIPELINE
# ---------------------------------------------------------
def main():
    img = get_user_input()
    if img is None:
        return
        
    print("\n--- Starting Phase 2 Processing Pipeline ---")
    
    # 1. Extract ROI
    print("1. Extracting Conjunctiva ROI...")
    roi = extract_conjunctiva_roi(img)
    
    # 2. Apply Fuzzy Logic Color Correction
    print("2. Applying Fuzzy Ambient-Light Correction...")
    corrected_roi = apply_fuzzy_correction(roi)
    
    # 3. Calculate Erythema Index
    print("3. Calculating Erythema Index...")
    raw_ei = calculate_erythema_index(roi)
    corrected_ei = calculate_erythema_index(corrected_roi)
    
    print(f"\n[Results]")
    print(f"Erythema Index (Before Correction): {raw_ei:.4f}")
    print(f"Erythema Index (After Correction) : {corrected_ei:.4f}")
    
    # Show Results side by side
    # Resize for display
    h = 200
    w = int((roi.shape[1] / roi.shape[0]) * h)
    roi_display = cv2.resize(roi, (w, h))
    corrected_display = cv2.resize(corrected_roi, (w, h))
    
    combined = np.hstack((roi_display, corrected_display))
    cv2.imshow("Left: Original ROI | Right: Fuzzy Corrected ROI", combined)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
