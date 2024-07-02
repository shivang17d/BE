const navbar = document.querySelector(".navbar");
const activeSticky = document.querySelector(".active-sticky");
const navHeight = navbar.getBoundingClientRect().height;

const sticky = function (entries) {
    const [entry] = entries;
    !entry.isIntersecting
        ? navbar.classList.add("sticky")
        : navbar.classList.remove("sticky");
};

const stickyNavObserver = new IntersectionObserver(sticky, {
    root: null,
    threshold: 1,
    rootMargin: `-${navHeight}px`,
});

stickyNavObserver.observe(activeSticky);


function voice() {
    var recognition = new webkitSpeechRecognition();
    recognition.lang = "en-GB";
    recognition.onresult = function (event) {
        console.log(event);
        document.getElementById("speechToText").value = event.results[0][0].transcript;
    }
    recognition.start();
}