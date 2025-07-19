export async function onRequest(context) {
  const { searchParams } = new URL(context.request.url);
  const code = searchParams.get('code');
  const { GITHUB_CLIENT_ID, GITHUB_CLIENT_SECRET } = context.env;

  const response = await fetch('https://github.com/login/oauth/access_token', {
    method: 'POST',
    headers: {
      'content-type': 'application/json',
      'user-agent': 'cloudflare-worker-decap-cms-oauth',
      'accept': 'application/json',
    },
    body: JSON.stringify({ client_id: GITHUB_CLIENT_ID, client_secret: GITHUB_CLIENT_SECRET, code }),
  });

  const result = await response.json();
  const_url = new URL(context.request.url)
  const url = `${_url.origin}/api/callback?token=${result.access_token}&scope=${result.scope}`

  return Response.redirect(url, 302);
}