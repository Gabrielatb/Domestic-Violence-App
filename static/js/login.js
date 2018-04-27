





// Iframe escape button
function toggleEscape() {
    
    if ( $("#myiframe").is("#myiframe:visible") ) {
        $("#myiframe").hide('#myiframe');
        }
    else {

        $("#myiframe").show('#myiframe');
    }
  
}
$("#escape_button").click(toggleEscape);


