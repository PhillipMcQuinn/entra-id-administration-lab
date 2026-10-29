import { PublicClientApplication, BrowserCacheLocation, InteractionRequiredAuthError } from '@azure/msal-browser';
const CLIENT='529b206d-0fd4-4d9e-a31e-19a9e6177158';
const API='487fb7d7-495e-4291-bf03-e0eba9367167';
const TENANT='2f3bd047-8146-4a8f-b7a9-f8f422392f6a';
const ORIGIN='http://localhost:3000';
const READ=`api://${API}/Inventory.Read`, WRITE=`api://${API}/Inventory.Write`;
const el=id=>document.getElementById(id);
let app, account=null, accessToken='', idToken='', recovery=false;
const ids=['login','read','write','missing','tamper','wrongaud','requestwrite','clear','logout'];
function busy(value){ for(const id of ids)el(id).disabled=value; }
function status(message){el('status').textContent=message;}
function row(target,label,value){const tr=document.createElement('tr');for(const s of [label,value]){const td=document.createElement('td');td.textContent=String(s);tr.append(td);}el(target).append(tr);}
function accept(result){account=result.account;app.setActiveAccount(account);accessToken=result.accessToken;idToken=result.idToken??'';status('Token acquired — '+account.username+'. Use the API tests below.');el('authresult').textContent=JSON.stringify({operation:'Acquire token',fromCache:result.fromCache,grantedScopes:result.scopes,correlationId:result.correlationId,time:new Date().toISOString()},null,2);}
function error(e){recovery=e.errorCode==='interaction_in_progress';status(recovery?'Close all Microsoft popups, then retry the sign-in or token request once.':'Authentication did not complete.');el('authresult').textContent=JSON.stringify({errorCode:e.errorCode??e.name??'unknown',entraError:String(e.errorMessage??e.message??'').match(/AADSTS\d+/)?.[0]??null,correlationId:e.correlationId??null,time:new Date().toISOString()},null,2);}
async function signIn(){busy(true);accessToken='';idToken='';status('Complete sign-in in the Microsoft window.');try{const overrideInteractionInProgress=recovery;recovery=false;accept(await app.loginPopup({scopes:[READ],prompt:'select_account',overrideInteractionInProgress}));}catch(e){error(e);}finally{busy(false);}}
async function acquire(scopes,forceRefresh=false){
  if(!account)throw new Error('Sign in first');
  try{return await app.acquireTokenSilent({account,scopes,forceRefresh});}
  catch(e){if(e instanceof InteractionRequiredAuthError){const overrideInteractionInProgress=recovery;recovery=false;return await app.acquireTokenPopup({account,scopes,overrideInteractionInProgress});}throw e;}
}
async function apiTest(label,method,token){
  const response=await fetch('/api/inventory',{method,headers:token?{Authorization:'Bearer '+token}:{},cache:'no-store',credentials:'omit'});
  const body=await response.json();
  el('latest').textContent=JSON.stringify({test:label,httpStatus:response.status,...body},null,2);
  const tr=document.createElement('tr');for(const v of [new Date().toLocaleTimeString(),label,response.status,body.error??body.result,body.requestId]){const td=document.createElement('td');td.textContent=String(v);tr.append(td);}el('history').prepend(tr);
  el('verified').replaceChildren();
  if(body.verifiedClaims){for(const [k,v] of Object.entries(body.verifiedClaims))row('verified',k,k==='exp'?new Date(v*1000).toISOString():v);}
  el('validation').textContent=body.tokenValidation==='passed'?'API verified signature, issuer, audience, lifetime, tenant, and token version. Authorization result: '+(body.error??body.result):'API did not accept this token. See the response below.';
  status(label+' — HTTP '+response.status);
}
async function run(label,method,kind){busy(true);try{
  let token='';
  if(kind==='read'){accept(await acquire([READ]));token=accessToken;}
  else if(kind==='current'){if(!accessToken){status('Sign in first to acquire the read token.');return;}token=accessToken;}
  else if(kind==='tamper'){if(!accessToken){status('Sign in first.');return;}const pieces=accessToken.split('.');pieces[2]=(pieces[2][0]==='A'?'B':'A')+pieces[2].slice(1);token=pieces.join('.');}
  else if(kind==='id'){if(!idToken){status('Sign in first.');return;}token=idToken;}
  await apiTest(label,method,token);
}catch(e){if(e.message==='Sign in first'){status('Sign in first.');}else if(e instanceof TypeError){status('Could not reach the local API. Keep the server window open.');}else error(e);}finally{busy(false);}}
async function requestWrite(){busy(true);status('Requesting a token with read and write scopes. Complete any Microsoft prompt.');try{accept(await acquire([READ,WRITE],true));}catch(e){error(e);}finally{busy(false);}}
async function clear(){busy(true);try{await app.clearCache();app.setActiveAccount(null);account=null;accessToken='';idToken='';el('verified').replaceChildren();el('validation').textContent='No token checked.';status('App cache cleared. Microsoft sign-in session may still be active.');}catch(e){error(e);}finally{busy(false);}}
async function logout(){busy(true);try{await app.logoutPopup({account:account??undefined,postLogoutRedirectUri:ORIGIN+'/'});account=null;accessToken='';idToken='';el('verified').replaceChildren();el('validation').textContent='No token checked.';status('Entra sign-out returned.');}catch(e){error(e);}finally{busy(false);}}
for(const [k,v] of Object.entries({'Client ID':CLIENT,'API audience':API,'Tenant ID':TENANT,'Read scope':READ,'Write scope (later stage)':WRITE,'SPA redirect URI':ORIGIN+'/','Authentication':'MSAL Browser 5.27.0 / Authorization Code with PKCE','API validation':'PyJWT 2.15.1 / RS256 / Entra public signing keys','Cache':'MSAL session storage; current test token held in memory'}))row('config',k,v);
el('login').onclick=signIn;el('read').onclick=()=>run('Read with access token','GET','read');el('write').onclick=()=>run('Write with current access token','POST','current');el('missing').onclick=()=>run('Read without a token','GET','none');el('tamper').onclick=()=>run('Read with tampered signature','GET','tamper');el('wrongaud').onclick=()=>run('Send client ID token to API','GET','id');el('requestwrite').onclick=requestWrite;el('clear').onclick=clear;el('logout').onclick=logout;
try{
 if(location.origin!==ORIGIN)throw new Error('Wrong origin');
 app=new PublicClientApplication({auth:{clientId:CLIENT,authority:`https://login.microsoftonline.com/${TENANT}`,redirectUri:ORIGIN+'/'},cache:{cacheLocation:BrowserCacheLocation.SessionStorage},system:{loggerOptions:{piiLoggingEnabled:false,loggerCallback:()=>{}}}});
 await app.initialize();account=app.getActiveAccount()??app.getAllAccounts()[0]??null;
 if(account)app.setActiveAccount(account);
 status(account?'Cached account available. Click Sign in for the baseline test.':'Ready — sign in to acquire Inventory.Read.');busy(false);
}catch(e){status('Startup failed. Open http://localhost:3000/lab.html and check the server.');}
