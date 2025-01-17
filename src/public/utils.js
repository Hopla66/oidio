filterChars = (str) => str.replace(/[\\"']/g, '\\$&').replace(/\u0000/g, '\\0')
// adds a css class to an HTML element		
const addClass = ( elt, add, className) => add ? elt.classList.add( className) : elt.classList.remove( className);
const showElement = ( elt, visible) =>  addClass( elt, !visible, "hiddenWidget");
const isVisible = (elt) => !elt.classList.contains("hiddenWidget");

const toggleIcon = (play) => { elt = document.querySelector('#play > i'); 
                             addClass( elt, play, 'fa-pause'); addClass( elt, !play, 'fa-play') }

//inject = (str, obj) => str.replace(/\${(.*?)}/g, (x,g)=> { return  eval( "obj."+g)});
//injectTemplate = (id, obj) => inject( TEMPLATES[id], obj)
//injectTemplateParent = (id, obj, p) => { t = injectTemplate(id, obj); p.insertAdjacentHTML('beforeend', t)}

clear = (x) =>{ while ( x.firstChild) { x.removeChild( x.lastChild);}  }

formatTime = (s) => (s == 0) ? "" : new Date(s * 1000).toISOString().slice(  (s > 3600 ? 11 : 14), 19)




async function callServer(url, params ) {
    console.log(`request [${params.method}] ${url} ...`);

    const response = await fetch (url, params);
    if( !response.ok) {
      const text = await response.text();
      throw new Error ( `Unable to fetch response for ${url} : ${response.status} - ${text}`);
    }
    return response.json();
  }  
  
  getRequest = (url) => callServer( url, { method: "GET"})
  postRequest = (url, params) => callServer( url, { body: params, method: "POST", headers: { Accept: "application/json", "Content-Type": "application/json" } })


 