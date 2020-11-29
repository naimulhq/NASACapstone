
function get_feed() {

  document.getElementById("Refresh").value="Hang on"
  var python = require("python-shell")
  var path = require("path")
  
  var options = {
    scriptPath : path.join(__dirname, '/Users/abelsemma/Project_Argus_GUI/engine'),
    pythonPath : '/usr/local/bin/python3'
  }

  var feed = new python3("layer.py",options);

 feed.end(function(err,code, message){
     document.getElementById("Refresh").value ="Refresh";
 })
}