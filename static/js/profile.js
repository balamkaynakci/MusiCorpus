const access_token = localStorage.getItem('access_token');

const recentSongsArea = document.getElementById('recent-songs');

async function getRecentSongs() {

    const songs = await fetch(`http://localhost:8888/profile/1/recently-played?access_token=${access_token}`);
    const songsJSON = await songs.json();
    if(songs.ok){
        songsJSON.forEach(element => {
            recentSongsArea.innerHTML += `<a href="${element.link}">${element.name}</a><br>`
        });
    }
    else{
        window.location = `http://localhost:8888/`;
    }
}

async function getFavSongs(){
    
}

getRecentSongs();
