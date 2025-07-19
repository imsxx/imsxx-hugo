export async function onRequest(context) {
  const { searchParams } = new URL(context.request.url);
  const token = searchParams.get('token');
  const scope = searchParams.get('scope');

  const content = `
    <!DOCTYPE html>
    <html lang="en">
      <head>
        <meta charset="utf-8" />
        <title>Authorizing ...</title>
      </head>
      <body>
        <script>
          const receive = (e) => {
            if (e.origin !== window.location.origin || e.data.auth !== 'decap_cms') return;
            window.removeEventListener('message', receive, false);
            e.source.postMessage(
              {
                auth: 'decap_cms',
                token: '${token}',
                scope: '${scope}',
              },
              e.origin
            );
          };
          window.addEventListener('message', receive, false);
          window.opener.postMessage({ auth: 'decap_cms' }, '*');
        </script>
      </body>
    </html>
  `;

  return new Response(content, {
    headers: { 'Content-Type': 'text/html;charset=UTF-8' },
  });
}