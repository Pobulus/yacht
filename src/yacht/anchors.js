
class Anchor {
    constructor(element, name, args){
        this.element = element;
        this.name = name;
        this.args = args;
    }       
}
class Anchors {

    anchors = [];
    pollingTargets = [];
    pollingDelay = 500;
    pollingInterval = null;
    bindAnchor(element, name, args, isPolling) {
        anchor = new Anchor(element, name, args)
        anchors.push(anchor);
        if (isPolling) pollingTargets.push(anchor);
    }
    poll() {
        pollingTargets.forEach(anchor => {
            console.log(anchor);
        });
    }
    startPolling() {
        pollingInterval = setInterval(poll, pollingDelay);
    }


}

var harbour = undefined;
(function () {
    harbour = new Anchors();

}())