class Timer {
    constructor( elt, formatter) {
        this.id = -1;
        this.elt = elt;
        this.formatter = formatter;
     }

    start = (duration, elapsed) => { 
        var display = document.querySelector( this.elt);
        if( display) {
            display.textContent = this.formatter(elapsed); 
            this.stop();
            if( elapsed < duration) {
                this.id = setTimeout( this.start, 1000, duration, ++elapsed);
            }
        }
    }

    stop = () => {
        if( this.id == -1) return;
         clearTimeout( this.id);
        this.id = -1;
    }
}