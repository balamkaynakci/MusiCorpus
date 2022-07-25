const signUpButton = document.getElementById('signup-button');



const authenticateSpotify = async () => {

    //send request to spotify including email 
    const url = await fetch(`/spotify/get-auth-url`);
    const urljson = await url.json();
    window.location = urljson.url;


}

//this function will activate when we click the sign up button

signUpButton.onclick = authenticateSpotify;