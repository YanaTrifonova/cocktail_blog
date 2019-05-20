/*Display one particular article that has been chosen by user*/

function articleDisplay(idToDisplay) {
    window.location.href = '/' + idToDisplay;

    let hiddenPrev = document.getElementById("prev");
    hiddenPrev.className += " paginations__hidden";

    let hiddenNext = document.getElementById("next");
    hiddenNext.className += " paginations__hidden";
}

