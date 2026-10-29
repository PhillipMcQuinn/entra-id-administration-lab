import { broadcastResponseToMainFrame } from '@azure/msal-browser/redirect-bridge';
broadcastResponseToMainFrame().catch(() => { document.querySelector('p').textContent = 'Open http://localhost:3000/lab.html to start the lab. This page receives sign-in results.'; });
