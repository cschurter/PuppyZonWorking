
//javascript
const findPetButton = d3.select('#FindPet');  


//on Button click event
findPetButton.on("click", function(){
    
    //Prevent the page from refreshing
    d3.event.preventDefault();

    //Get the user input data
    var animalType = d3.select('#animalType').property("value");


    //BreedName
    var breedName = d3.select('#BreedName').property("value");
    //zipcode
    var zipcode = d3.select('#zipcode').property("value");
    
    console.log("Animal Type is " + animalType);
    console.log("Breed Type is " + breedName);
    console.log("zipcode is " + zipcode);

    //Call the API with these 3 parameters

});


// //File Browse Button click event
const browseButton = document.getElementById('browse');
const fileDialogBox = document.getElementById('file');
const spanText = document.getElementById('custom-text');

browseButton.addEventListener("click", function(){
    fileDialogBox.click();
});

fileDialogBox.addEventListener("change", function(){
    if(fileDialogBox.value){
        spanText.innerHTML = fileDialogBox.value.match(/[\/\\]([\w\d\s\.\-(\)]+)$/)[1];
     
        if (this.files && this.files[0]){
            var obj = new FileReader();
            obj.onload = function(data){
                var image = document.getElementById('uploadedImg');
                image.src = data.target.result;
                image.style.display =  "block";
            }
            obj.readAsDataURL (this.files[0]);
        }
     
     
        // var imgShow = document.getElementById('uploadedImg');
        // // console.log("imgShow.display: "+ imgShow);
        // imgShow.src = "../static/images/Dog3.jpg" 
        // imgShow.display = "block";

        // // if (imgShow.display === "none"){
        // //     imgShow.display = "block";
        // // }
        // // else {
        // //     imgShow.display = "none";
        // }
    }
    else{
        spanText.innerHTML="No file chosen"
    }
    
});


