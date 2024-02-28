class Anchor {
    constructor(element, name, args, target){
        this.element = element;
        this.name = name;
        this.args = args;
        this.target = target;
        this.redirect = undefined;
    }      
    addRedirect(href) {
        this.redirect = href;
    }
    send() {
        const xhr = new XMLHttpRequest();
        xhr.open("POST", `http://${window.location.host}/anchor/${this.name}`);
        xhr.send(JSON.stringify({
            value: this.element.value,
            arguments: this.args
        }));
        xhr.responseType = "text";
        xhr.onload = () => {
            if (xhr.readyState == 4 && xhr.status == 200) {
                if (xhr.responseText) {
                    if(this.target === 'href'){window.location.href = xhr.responseText;}
                    else{if(this.target === 'redirect'){window.location.replace(xhr.responseText);}}
                }
                if(this.target){this.element[this.target] = xhr.responseText;}
            } else {
                console.log(`Error: ${xhr.status}`);
                console.log(`happended on anchor: ${this}`);
            }
        };
    }
}
class Anchors {
    anchors = [];
    pollingTargets = [];
    pollingDelay = 500;
    pollingInterval = null;
    bindAnchor(id, name, args, target, trigger, redirect) {
        const anchor = new Anchor(document.getElementById(id), name, args, target);
        this.anchors.push(anchor);
        if (trigger === 'always') {this.pollingTargets.push(anchor);}
        if(redirect) {
            anchor.addRedirect(redirect);
        }
        if(trigger) {
            if(trigger === 'once' || trigger === 'always'){
                anchor.send();
            }else {
                const previousFunction = document.getElementById(id)[trigger];
                document.getElementById(id)[trigger] = function() {
                    if(previousFunction) previousFunction();    
                    anchor.send();
                }
            }
        }
    }
    request(harb) {
        harbour.pollingTargets.forEach(anchor => {
            anchor.send();            
        });
    }
    startPolling() {
        clearInterval(this.pollingInterval);
        this.pollingInterval = setInterval(function() {harbour.request();}, this.pollingDelay);
    }
}

var harbour = undefined;
(function () {
    harbour = new Anchors();
    document.addEventListener("DOMContentLoaded", function(event) {
        harbour.startPolling();
    }); 
}())