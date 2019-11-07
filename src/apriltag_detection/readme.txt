Inside apriltag_detection:

    1. AprilTag detection.ipynb -- The jupyter notebook containing:
          - all necessary code
          - some additional implementations marked optional or skip (ones that I implemented for debbugging purposes)
    
    2. calibration_images -- a folder containing images from a webcam (Microsoft LifeCam HD-3000) and from a wide angle camera (Pixel3 Wide angle front -- for distortion debbuging purposes)
    
    3. apriltags3-py -- A python wrapper to the apriltags C++ implementation. https://github.com/duckietown/apriltags3-py
    

Instructions:

Before using this notebook:
    1. clone apriltags3-py from github: https://github.com/duckietown/apriltags3-py
    
    2. open notebook and use "Section 1" to take new pictures of chessboard and apriltags using your webcam (or use ones in calibration_images)
    
    3. override the "path_to_image" and "path_to_library" variables in the notebook to the path for the library you cloned in part 1, and the image locations.
    
    4. You will need to pip install opencv, numpy, and more. A requirements.txt file contains all the packages needed to rebuild my virtualenv. Follow instructions in https://developer.akamai.com/blog/2017/06/21/how-building-virtual-python-environment
    
             
             
            
             
             


WebCam Model: https://www.amazon.com/Microsoft-LifeCam-HD-3000-for-Business/dp/B005BZNEKM/ref=asc_df_B005BZNEKM/?tag=hyprod-20&linkCode=df0&hvadid=309818716690&hvpos=1o4&hvnetw=g&hvrand=9386433060891322298&hvpone=&hvptwo=&hvqmt=&hvdev=c&hvdvcmdl=&hvlocint=&hvlocphy=9003488&hvtargid=aud-801381245258:pla-338189077186&psc=1
