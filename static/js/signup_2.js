const url = 'http://localhost:8888/signup';

const signUpButton = document.getElementById("submit-button");
const email_signup = document.getElementById('email-signup');
const signup_message = document.getElementById('signup-message');
const gender_signup = document.getElementById('gender-signup');
const city_signup = document.getElementById('city-signup');
const password_1_signup= document.getElementById('password1-signup');
const password_2_signup= document.getElementById('password2-signup');

const signUp = async () =>{
    // Initially, studentId and bookId are string. But, they need to be number to use it.

    const city_value = city_signup.value;
    const email_value = email_signup.value;
    const password1_value = password_1_signup.value;
    const password2_value = password_2_signup.value;
    const gender_value = gender_signup.value;
    console.log('city',city_value);
    console.log('email',email_value);
    console.log('passw',password1_value);
    console.log('gender',gender_value);

    //all these inputs shouldn't be empty
    if(email_value === "" || password1_value === "" || password2_value === "" || city_value==="" || gender_value === ""){
        //message will be sended from html
        console.log("empty")
        return;
    }

    //check passwords:
    if(password1_value !== password2_value){
        signup_message.innerHTML = 'Passwords should match';
        return;
    }

    const params = new URLSearchParams(window.location.search)
    access_token = params.get('access_token');
    refresh_token = params.get('refresh_token');
    console.log(access_token, refresh_token)
    const fetchToUrl = url;

    try{
        console.log(1);
        const createUser = await fetch(fetchToUrl, {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
              },
            body:JSON.stringify({
                access_token:access_token,
                refresh_token: refresh_token,
                email:email_value,
                gender:gender_value,
                city:city_value,
                password:password1_value})
        });

        if(createUser.ok){
            console.log(3);
            const createUserJSON = await createUser.json();
            console.log(createUserJSON);
            localStorage.setItem('access_token',access_token);
            localStorage.setItem('refresh_token',refresh_token);
            window.location = 'http://localhost:8888/main'
        }
        else{
            window.location = 'http://localhost:8888/'
        }
    }
    catch(error){
        console.log(4);
        console.log(error);
    }
    
}


signUpButton.onclick = signUp;
