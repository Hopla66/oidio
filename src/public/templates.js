
class Template {
    constructor( filename) {
        this.templates = [];
        this.load( filename);
    }

    load= (file) => {
        const request = new XMLHttpRequest();
        request.open("GET", "./"+file, false); // `false` makes the request synchronous
        request.send(null);

        if (request.status === 200) {
             var elt = document.createElement("div");
             elt.innerHTML = request.responseText;

        
            var initTemplate = (tpl) => { this.templates[tpl.id] = doT.template( tpl.innerHTML); console.log("created "+tpl.id)}
        
            elt.querySelectorAll("script").forEach( x => initTemplate(x))
       }
    }

    clear = (x) =>{ while ( x.firstChild) { x.removeChild( x.lastChild);}  }

    inject = (id, obj) => this.templates[id](obj)

    injectParent = (id, obj, p, clearFlag = true) => {
        if( clearFlag) {
            this.clear( p)
        }
        p.insertAdjacentHTML('beforeend', this.inject(id,obj));
        return p;
    }

}

