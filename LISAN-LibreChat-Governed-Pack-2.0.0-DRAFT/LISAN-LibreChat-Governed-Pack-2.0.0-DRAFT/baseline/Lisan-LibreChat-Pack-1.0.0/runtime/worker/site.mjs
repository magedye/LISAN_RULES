/** Portable Site composition. Operator supplies the REAL verified host principal.
No HTTP actor/header/user-supplied ID constitutes an authenticator. Default is blocked. */
import blocked,{createApplication} from './index.mjs';
import assets from './ui_assets.mjs';
const mime={'/':'text/html','/ui.css':'text/css','/ui.mjs':'text/javascript'};
export function createSiteApplication({authenticate,allowedOrigin,protocol}={}) {
  if(typeof authenticate!=='function'||!allowedOrigin)return blocked.fetch;
  const api=createApplication({authenticate,allowedOrigin,protocol});
  return async request=>{
    const url=new URL(request.url),origin=request.headers.get('origin');
    if(url.origin!==allowedOrigin||(origin&&origin!==allowedOrigin))return new Response('ORIGIN_NOT_ALLOWED',{status:403});
    if(!Object.hasOwn(assets,url.pathname))return api(request);
    let p;try{p=await authenticate(request);}catch{return new Response('AUTHENTICATION_REQUIRED',{status:401});}
    if(!p?.subject||p.owner!==true||p.scope!=='research:read')return new Response('ACCESS_DENIED',{status:403});
    if(request.method!=='GET')return new Response('METHOD_NOT_ALLOWED',{status:405});
    // Browser posts remain same-origin and authenticated by the host on EVERY request.
    const html=assets[url.pathname].replace('__CSRF__','');
    return new Response(html,{headers:{'Content-Type':mime[url.pathname]+'; charset=utf-8','Cache-Control':'no-store','X-Content-Type-Options':'nosniff','Referrer-Policy':'no-referrer','Content-Security-Policy':"default-src 'none'; script-src 'self'; style-src 'self'; connect-src 'self'; font-src 'none'; img-src 'self'; object-src 'none'; base-uri 'none'; form-action 'self'; frame-ancestors 'none'"}});
  };
}
export default blocked;
