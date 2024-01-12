function getGoogleAuthURL(elementId) {
  const rootUrl = 'https://accounts.google.com/o/oauth2/v2/auth';

  // Check the elementId and update redirect_uri accordingly
  if (elementId === 'signup') {
    var redirect_uri = 'http://localhost:5000/user/signup';
  } else if (elementId === 'login') {
    var redirect_uri = 'http://localhost:5000/user/login';
  } else {
    // Default redirect_uri if elementId is not recognized
    var redirect_uri = 'http://localhost:5000/user/signup';
  }

  const options = {
    redirect_uri,
    client_id: '471431009289-outsbp3gmvr1mfujip5l3lb6lvhji0m1.apps.googleusercontent.com',
    access_type: 'offline',
    response_type: 'code',
    prompt: 'consent',
    scope: [
      'https://www.googleapis.com/auth/userinfo.profile',
      'https://www.googleapis.com/auth/userinfo.email',
      'https://www.googleapis.com/auth/contacts.other.readonly',
      'https://www.googleapis.com/auth/calendar',
      'https://www.googleapis.com/auth/calendar.events'
    ].join(' '),
  };

  const qs = new URLSearchParams(options);

  console.log(qs.toString());

  return `${rootUrl}?${qs.toString()}`;
}
