var harbour = undefined;

class Anchor {
  constructor(element, name, args, target) {
    this.element = element;
    this.name = name;
    this.args = args;
    this.target = target;
  }
  updateTarget(response) {
    if (response) {
      if (this.target === "href") {
        window.location.href = response;
      } else if (this.target === "redirect") {
        window.location.replace(response);
      }
    }
    if (this.target) {
      this.element[this.target] = response;
    }
  }
  compareArgs(other) {
    return this.args
      ? Object.keys(this.args).filter(
          (key) => other[key] && other[key] === this.args[key]
        ).length === Object.keys(this.args).length
      : true;
  }
  send() {
    const xhr = new XMLHttpRequest();
    xhr.open("POST", `http://${window.location.host}/anchor/${this.name}`);
    xhr.send(
      JSON.stringify({
        value: this.element.value,
        arguments: this.args,
      })
    );
    xhr.responseType = "text";
    xhr.onload = () => {
      if (xhr.readyState == 4 && xhr.status == 200) {
        this.updateTarget(xhr.responseText);
        if (this.name in harbour.chainedAnchors) {
          harbour.chainedAnchors[this.name].forEach((a) => {
            if (a.compareArgs(this.args)) a.updateTarget(xhr.responseText);
          });
        }
      } else {
        console.log(`Error: ${xhr.status}`);
        console.log(`happended on anchor: ${this}`);
      }
    };
  }
}
class Harbour {
  anchors = [];
  pollingTargets = [];
  chainedAnchors = {};
  pollingDelay = 500;
  pollingInterval = null;
  bindAnchor(id, name, args, target, trigger) {
    const anchor = new Anchor(document.getElementById(id), name, args, target);
    this.anchors.push(anchor);
    if (trigger === "always") {
      this.pollingTargets.push(anchor);
    } else if (trigger === "chain") {
      if (!(name in this.chainedAnchors)) {
        this.chainedAnchors[name] = [];
      }
      this.chainedAnchors[name].push(anchor);
    }
    if (trigger) {
      if (trigger === "once" || trigger === "always") {
        anchor.send();
      } else {
        const previousFunction = document.getElementById(id)[trigger];
        document.getElementById(id)[trigger] = function () {
          if (previousFunction) previousFunction();
          anchor.send();
        };
      }
    }
  }
  request(harb) {
    harbour.pollingTargets.forEach((anchor) => {
      anchor.send();
    });
  }
  startPolling() {
    clearInterval(this.pollingInterval);
    this.pollingInterval = setInterval(function () {
      harbour.request();
    }, this.pollingDelay);
  }
}

(function () {
  harbour = new Harbour();
  document.addEventListener("DOMContentLoaded", function (event) {
    harbour.startPolling();
  });
})();
