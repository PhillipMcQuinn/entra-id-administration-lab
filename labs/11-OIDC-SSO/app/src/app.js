import { PublicClientApplication, BrowserCacheLocation } from '@azure/msal-browser';

const CLIENT = '0ab52627-9b78-4bb9-b721-82916d824e69';
const TENANT = '2f3bd047-8146-4a8f-b7a9-f8f422392f6a';
const ORIGIN = 'http://localhost:3000';
const REDIRECT = ORIGIN + '/';
const ISSUER = `https://login.microsoftonline.com/${TENANT}/v2.0`;
const el = id => document.getElementById(id);
const buttons = ['login','clear','logout','mismatch'];
let app, currentAccount = null, recoverInteraction = false;
function status(message){ el('status').textContent = message; }
function busy(value){ for(const id of buttons)el(id).disabled = value; }
function row(target, label, value){
  const tr=document.createElement('tr');
  for(const v of [label,value]){const td=document.createElement('td');td.textContent=String(v);tr.append(td);}
  el(target).append(tr);
}
function short(v){ return typeof v === 'string' ? v.slice(0,8) + '… (masked)' : 'Not present'; }
function clearDisplay(){ el('claims').replaceChildren();el('claimnote').textContent='No claims displayed. Sign in for a new result.'; }
function display(account, claims, fresh){
  clearDisplay();
  el('claimnote').textContent = fresh ? 'Claims from the latest completed MSAL sign-in. The checks below are teaching comparisons, not an independent signature-validation report.' : 'Cached account claims restored after refresh. This is not evidence of a new Entra sign-in.';
  for(const [k,v] of Object.entries({name:claims.name??'(not supplied)',preferred_username:claims.preferred_username??account.username,iss:claims.iss,aud:claims.aud,tid:claims.tid,sub:short(claims.sub),oid:short(claims.oid),nonce:short(claims.nonce),roles:Array.isArray(claims.roles)?claims.roles.join(', '):'No app roles in this token',exp:claims.exp?new Date(claims.exp*1000).toISOString():'Not present'}))row('claims',k,v);
  const checks = { 'Audience equals client ID':claims.aud===CLIENT, 'Issuer equals tenant v2 issuer':claims.iss===ISSUER,'Tenant matches registration':claims.tid===TENANT,'Token expiry is in the future':Number.isFinite(claims.exp)&&claims.exp*1000>Date.now(),'Subject is present':typeof claims.sub==='string'&&claims.sub.length>0};
  for(const [k,v] of Object.entries(checks))row('claims',k,v?'PASS':'FAIL');
  const valid=Object.values(checks).every(Boolean);
  status(valid ? (fresh?'Sign-in completed — '+account.username:'Cached account — '+account.username) : 'Claim comparison failed — inspect the displayed values.');
}
function reportError(error, operation){
  recoverInteraction = error.errorCode === 'interaction_in_progress';
  status(recoverInteraction ? 'Previous interaction is still active. Close Microsoft popups, then click Sign in again to recover.' : operation+' did not complete.');
  // Restrict output to identifiers, not raw errors that could contain authentication data.
  const aadsts=String(error.errorMessage??error.message??'').match(/AADSTS\d+/)?.[0];
  el('diagnostics').textContent=JSON.stringify({operation,result:'Not completed',errorCode:error.errorCode??error.name??'unknown',entraError:aadsts??'See Microsoft sign-in window',subError:error.subError??null,correlationId:error.correlationId??null,time:new Date().toISOString()},null,2);
}
async function login(mismatch=false){
  busy(true);clearDisplay();status('Complete sign-in in the Microsoft window.');
  try{
    const overrideInteractionInProgress = recoverInteraction;
    recoverInteraction = false;
    const result=await app.loginPopup({overrideInteractionInProgress,scopes:['openid','profile'],prompt:'select_account',redirectUri:mismatch?ORIGIN+'/unregistered-callback.html':REDIRECT});
    currentAccount=result.account;app.setActiveAccount(currentAccount);
    display(currentAccount,result.idTokenClaims??{},true);
    el('diagnostics').textContent=JSON.stringify({operation:mismatch?'Mismatch test':'Sign-in',result:'MSAL completed',fromCache:result.fromCache,correlationId:result.correlationId,time:new Date().toISOString()},null,2);
  }catch(e){reportError(e,mismatch?'Mismatch test':'Sign-in');}finally{busy(false);}
}
async function clearLocal(){
  busy(true);
  try{await app.clearCache();currentAccount=null;app.setActiveAccount(null);clearDisplay();status('App cache cleared. Microsoft session may still be active.');el('diagnostics').textContent='Local cache cleared; no Entra session sign-out was requested.';}catch(e){reportError(e,'Clear app cache');}finally{busy(false);}
}
async function logout(){
  busy(true);
  try{
    await app.logoutPopup({account:currentAccount??undefined,postLogoutRedirectUri:REDIRECT});
    currentAccount=null;clearDisplay();status('Entra sign-out returned. Verify session behavior with another sign-in.');
  }catch(e){reportError(e,'Entra sign-out');}finally{busy(false);}
}
for(const [k,v] of Object.entries({'Client ID':CLIENT,'Tenant ID':TENANT,'Authority':`https://login.microsoftonline.com/${TENANT}`,'SPA redirect URI':REDIRECT,'Library':'Microsoft MSAL Browser 5.27.0','Requested scopes':'openid profile','Cache':'Session storage'}))row('config',k,v);
el('login').onclick=()=>login(false);el('mismatch').onclick=()=>login(true);el('clear').onclick=clearLocal;el('logout').onclick=logout;
try{
  if(location.origin!==ORIGIN)throw new Error('Open http://localhost:3000/lab.html');
  app=new PublicClientApplication({auth:{clientId:CLIENT,authority:`https://login.microsoftonline.com/${TENANT}`,redirectUri:REDIRECT},cache:{cacheLocation:BrowserCacheLocation.SessionStorage},system:{loggerOptions:{piiLoggingEnabled:false,loggerCallback:()=>{}}}});
  await app.initialize();
  currentAccount=app.getActiveAccount()??app.getAllAccounts()[0]??null;
  if(currentAccount){app.setActiveAccount(currentAccount);display(currentAccount,currentAccount.idTokenClaims??{},false);}else status('Ready — no account selected.');
  busy(false);
}catch(e){status(e.message==='Open http://localhost:3000/lab.html'?e.message:'Authentication library initialization failed.');reportError(e,'Startup');}
