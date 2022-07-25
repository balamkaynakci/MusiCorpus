const access_token_input = document.getElementById("access-token");
const refresh_token_input = document.getElementById("refresh-token");

const params = new URLSearchParams(window.location.search)
access_token = params.get('access_token');
refresh_token = params.get('refresh_token');

access_token_input.setAttribute('value',access_token);
refresh_token_input.setAttribute('value',refresh_token);
