/*Declare time*/
const countToDate = new Date().setDate(new Date().getDate() + 9);

/*Calculate time from current date compared to the Declared time*/
setInterval(() => {
  const currentDate = new Date();
  const timeBetweenDates = Math.ceil((countToDate - currentDate) / 1000);
  flipAllcard(timeBetweenDates);
}, 250);


/*Populate the cards with the data coming from the Declared Time*/
function flipAllcard(time) {
  const seconds = time % 60;
  const minutes = Math.floor(time / 60) % 60;
  const hours = Math.floor(time / 3600) % 24;
  const days = Math.floor(time / 86400);

  flip(document.querySelector("[data-days]"), days, true);
  flip(document.querySelector("[data-hours]"), hours);
  flip(document.querySelector("[data-minutes]"), minutes);
  flip(document.querySelector("[data-seconds]"), seconds);
}


/*Flip animation function for the cards*/
function flip(flipcard, newNumber, flag) {
    const cardTop = flipcard.querySelector("[data-card-top]");
    const startNumber = cardTop ? parseInt(cardTop.textContent, 10) : 0;
  
    const cardBot = flipcard.querySelector("[data-card-bot]"),
      topFlip = flipcard.querySelector("[data-flip-top]"),
      botFlip = flipcard.querySelector("[data-flip-bot]"),
      topFlipNum = flipcard.querySelector("[data-flip-top-num]"),
      botFlipNum = flipcard.querySelector("[data-flip-bot-num]");

  if (newNumber === startNumber) return;

  const displayStartNum = String(startNumber).padStart(2, "0");

  const displayNewNum = String(newNumber).padStart(2, "0");

  if (flag) console.log("displayStartNum", displayStartNum, displayNewNum);

  const anim = (el, event, callback) => {
    const handler = () => {
      el.removeEventListener(event, handler);
      callback();
    };

    el.addEventListener(event, handler);
  };

  cardTop.textContent = displayStartNum;
  cardBot.textContent = displayStartNum;
  topFlipNum.textContent = displayStartNum;
  botFlipNum.textContent = displayNewNum;

  topFlip.classList.add("flip-card-top");
  botFlip.classList.add("flip-card-bottom");

  anim(topFlip, "animationstart", () => {
    cardTop.textContent = displayNewNum;
  });

  anim(topFlip, "animationend", () => {
    topFlipNum.innerText = displayNewNum;
    topFlip.classList.remove("flip-card-top");
  });

  anim(botFlip, "animationend", () => {
    cardBot.textContent = displayNewNum;
    botFlip.classList.remove("flip-card-bottom");
  });
}
