// Funtion to acknowledge the loading of opencv.js so it will not throw error.
function openCvReady() {
  cv['onRuntimeInitialized'] = () => {
    console.log("opencv is Ready.");
  }
}

// Funtion to convert image to Cartoon.
function imagetocartoon() {
  video = document.getElementById("cam_input"); // cam_input is the id of video tag

  // Get media stream from user's media and play in cam_input tag
  navigator.mediaDevices.getUserMedia({ video: true, audio: false })
    .then(function (stream) {
      video.srcObject = stream;
      video.play();
    })
    .catch(function (err) {
      console.log("An error occurred! " + err);
    });

  // Declaring Variables to have source and destination image in cv.Mat with same width and height as video tag.
  let src = new cv.Mat(video.height, video.width, cv.CV_8UC4);
  let dst = new cv.Mat(video.height, video.width, cv.CV_8UC1);

  // Declaring supporting variables required to cartoonify in cv.Mat.
  let gray = new cv.Mat();
  let edge = new cv.Mat();
  let blur = new cv.Mat();

  // Capture the Video by opencv with source from video tag(cam_input).
  let cap = new cv.VideoCapture(cam_input);

  // Set the Frame per Second to recall the function after it finished.
  const FPS = 24;

  // Function for the processing image from cam(video tag) and cartoonify it.
  function processVideo() {
    let begin = Date.now();
    
    // Reading image from cap(opencv) and store it in src. 
    cap.read(src);
    src.copyTo(dst);

    // To avoid and error try catch block is used for cartoonify.
    try {

      // Converting src image to float array for processing.
      let mat = src;
      cv.convertScaleAbs(mat,mat, alpha=1.9, beta=1)
      let sample = new cv.Mat(mat.rows * mat.cols, 3, cv.CV_32F);
      for (var y = 0; y < mat.rows; y++)
        for (var x = 0; x < mat.cols; x++)
          for (var z = 0; z < 3; z++)
            sample.floatPtr(y + x * mat.rows)[z] = mat.ucharPtr(y, x)[z];

      // Declaring  variable like cluster attempts for K Means algorithm.
      var clusterCount = 20;
      var labels = new cv.Mat();
      var attempts = 0;
      var centers = new cv.Mat();

      // Seting the criteria for k means. 
      var crite = new cv.TermCriteria(cv.TermCriteria_EPS + cv.TermCriteria_MAX_ITER, 10, 1.0);

      // Apply Kmeans and store it centers.
      cv.kmeans(sample, clusterCount, labels, crite, attempts, cv.KMEANS_RANDOM_CENTERS, centers);

      // Converting Back the float array to cv.mat(newImage).
      var newImage = new cv.Mat(mat.size(), mat.type());
      for (var y = 0; y < mat.rows; y++)
        for (var x = 0; x < mat.cols; x++) {
          var cluster_idx = labels.intAt(y + x * mat.rows, 0);
          var redChan = new Uint8Array(1);
          var greenChan = new Uint8Array(1);
          var blueChan = new Uint8Array(1);
          var alphaChan = new Uint8Array(1);
          redChan[0] = centers.floatAt(cluster_idx, 0);
          greenChan[0] = centers.floatAt(cluster_idx, 1);
          blueChan[0] = centers.floatAt(cluster_idx, 2);
          alphaChan[0] = 255;
          newImage.ucharPtr(y, x)[0] = redChan;
          newImage.ucharPtr(y, x)[1] = greenChan;
          newImage.ucharPtr(y, x)[2] = blueChan;
          newImage.ucharPtr(y, x)[3] = alphaChan;
        }
      
      
      // Convert newImage to Gray Scale image.
      cv.cvtColor(src, gray, cv.COLOR_RGB2GRAY, 0);
      // Smoothin newImage by median blur.
      cv.medianBlur(newImage, blur, 3)
      // Edge detection by adaptiveThreshold from gray to edge.
      cv.adaptiveThreshold(gray, edge, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY, 9, 9);
      // Adding result of blur and edge.
      cv.bitwise_and(blur, blur, dst, mask = edge)
      // Display the cartoon image in canvas(canvas_output).
      cv.imshow("canvas_output", dst);
    }
    catch (err) {
      console.log(err);
    }
    // schedule next one.
    let delay = 1000 / FPS - (Date.now() - begin);
    setTimeout(processVideo, delay);
  }
  // schedule first one.
  setTimeout(processVideo, 10);
}

// Start function of cartoonify project
function start_cartoon() {
  // Getting user Permission
  var cama = navigator.mediaDevices && navigator.mediaDevices.getUserMedia;
  // If permission is given start converting.
  if (cama) {
    imagetocartoon();
  }
  // If permission is not given prompting a message.
  else{
    prompt("Permission is denied so can not convert image to cartoon.");
  }
}

// fuction of stop button of cartoonify project.
function stop_cartoon() {
  video.pause();
}

// Fuction of download Cartoonify Image.
function download_cartoon() {
  stop_cartoon();
  var link = document.createElement('a');
  link.download = 'cartoonImgFromRahul.png';
  link.href = document.getElementById('canvas_output').toDataURL()
  link.click();
}