function getGoogleAuthURL() {
  const rootUrl = 'https://accounts.google.com/o/oauth2/v2/auth';

  const options = {
    redirect_uri: 'http://localhost:5000/user/login',
    client_id: '471431009289-outsbp3gmvr1mfujip5l3lb6lvhji0m1.apps.googleusercontent.com',
    access_type: 'offline',
    response_type: 'code',
    prompt: 'consent',
    scope: [
      'https://www.googleapis.com/auth/userinfo.profile',
      'https://www.googleapis.com/auth/userinfo.email',
    ].join(' '),
  };

  console.log(options);

  const qs = new URLSearchParams(options);

  console.log(qs.toString());

  return `${rootUrl}?${qs.toString()}`;
}
