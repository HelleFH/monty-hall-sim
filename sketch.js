const doors = [];
const carImage = 'car.png'; // Adjust path as per your file structure
const goatImage = 'goat.png'; // Adjust path as per your file structure

let totalDoors = 3;

let state = 'PICK';
let pickedDoor;

let autoMode = false;
let timeoutId;

let stats = {
  totalSwitchPlays: 0,
  totalStayPlays: 0,
  totalSwitchWins: 0,
  totalStayWins: 0,
};

function getDelayValue() {
  const speedSlider = select('#speed-slider');
  return speedSlider.elt.max - speedSlider.value();
}

function clearStats() {
  stats = {
    totalSwitchPlays: 0,
    totalStayPlays: 0,
    totalSwitchWins: 0,
    totalStayWins: 0,
  };
  clearStorage();
  updateStats();
}

function reset() {
  for (const door of doors) {
    door.prize = goatImage;
    door.revealed = false;
    select('.door', door).html(door.index + 1);
    select('.content', door).html(''); 
    door.removeClass('revealed');
    door.removeClass('picked');
    door.removeClass('won');
  }

  const winner = random(doors);
  winner.prize = carImage; // Set the winner's prize to the train image

  state = 'PICK';
  select('#instruction > p').html('Pick a Door!');
  select('#instruction > .choices').hide();
  select('#instruction > #play-again').hide();

  if (autoMode) {
    timeoutId = setTimeout(pickDoor, getDelayValue());
  }
}

function updateStats() {
  // Calculate switch win rate
  const switchWinRate = nf((100 * stats.totalSwitchWins) / stats.totalSwitchPlays || 0, 2, 1) + '%';
  
  // Update switch statistics
  document.querySelector('#stats #switches .total').innerHTML = stats.totalSwitchPlays;
  document.querySelector('#stats #switches .bar').style.width = switchWinRate;
  document.querySelector('#stats #switches .win-rate').innerHTML = switchWinRate;
  document.querySelector('#stats #switches .wins-switch').innerHTML = stats.totalSwitchWins;

  // Calculate stay win rate
  const stayWinRate = nf((100 * stats.totalStayWins) / stats.totalStayPlays || 0, 2, 1) + '%';
  
  // Update stay statistics
  document.querySelector('#stats #stays .total').innerHTML = stats.totalStayPlays;
  document.querySelector('#stats #stays .bar').style.width = stayWinRate;
  document.querySelector('#stats #stays .win-rate').innerHTML = stayWinRate;
  document.querySelector('#stats #stays .wins-stay').innerHTML = stats.totalStayWins;

  // Update total games played
  const totalGamesPlayed = stats.totalSwitchPlays + stats.totalStayPlays;
  document.querySelector('#total-games .total-games').innerHTML = totalGamesPlayed;
  // Calculate and update total wins
  const totalWins = stats.totalSwitchWins + stats.totalStayWins;
  document.querySelector('#total-wins .total-wins').innerHTML = totalWins;
}
function updateStats() {
  // Calculate switch win rate percentage
  const switchWinRatePercent = (100 * stats.totalSwitchWins) / stats.totalSwitchPlays || 0;
  const switchWinRate = nf(switchWinRatePercent, 2, 1) + '%';

  // Update switch statistics
  document.querySelector('#stats #switches .total').innerHTML = stats.totalSwitchPlays;
  document.querySelector('#stats #switches .bar').style.width = switchWinRate;
  document.querySelector('#stats #switches .win-rate').innerHTML = switchWinRate;
  document.querySelector('#stats #switches .wins-switch').innerHTML = stats.totalSwitchWins;

  // Calculate stay win rate percentage
  const stayWinRatePercent = (100 * stats.totalStayWins) / stats.totalStayPlays || 0;
  const stayWinRate = nf(stayWinRatePercent, 2, 1) + '%';

  // Update stay statistics
  document.querySelector('#stats #stays .total').innerHTML = stats.totalStayPlays;
  document.querySelector('#stats #stays .bar').style.width = stayWinRate;
  document.querySelector('#stats #stays .win-rate').innerHTML = stayWinRate;
  document.querySelector('#stats #stays .wins-stay').innerHTML = stats.totalStayWins;

  // Calculate and update total games played
  const totalGamesPlayed = stats.totalSwitchPlays + stats.totalStayPlays;
  document.querySelector('#total-games .total-games').innerHTML = totalGamesPlayed;

  // Calculate and update total wins
  const totalWins = stats.totalSwitchWins + stats.totalStayWins;
  document.querySelector('#total-wins .total-wins').innerHTML = totalWins;

  // Update circular charts
  updateCircularProgressBar('#switches .circular-chart.orange', switchWinRatePercent, '#ff9f00'); // Orange color
  updateCircularProgressBar('#stays .circular-chart.green', stayWinRatePercent, '#4cc790'); // Green color
}

function updateCircularProgressBar(selector, percentage, progressColor) {
  const circle = document.querySelector(selector + ' .circle');
  const circumference = circle.getTotalLength();
  const offset = circumference - (percentage / 100) * circumference;
  
  circle.style.stroke = progressColor;
  circle.style.strokeDasharray = `${percentage} ${100 - percentage}`;
  circle.style.strokeDashoffset = offset;
  
  document.querySelector(selector + ' .percentage').innerHTML = `${percentage.toFixed(1)}%`;
}

function checkWin(hasSwitched) {
  for (const door of doors) {
    door.addClass('revealed');
    // Display prize image instead of text
    select('.content', door).html(`<img src="${door.prize}">`);
  }

  if (pickedDoor.prize === carImage) {
    pickedDoor.addClass('won');
    if (hasSwitched) {
      stats.totalSwitchWins++;
    } else {
      stats.totalStayWins++;
    }
    select('#instruction > p').html('You win!');
  } else {
    select('#instruction > p').html('You lose!');
  }

  if (autoMode) {
    timeoutId = setTimeout(reset, getDelayValue());
  } else {
    select('#instruction > #play-again').show();
  }

  updateStats();
  storeItem('montey-hall-stats', stats);
}

function chooseDoor(hasSwitched = false) {
  select('#instruction > .choices').hide();

  if (hasSwitched) {
    stats.totalSwitchPlays++;
    const newPick = doors.find(
      (door) => !door.hasClass('revealed') && !door.hasClass('picked')
    );
    newPick.addClass('picked');
    pickedDoor.removeClass('picked');
    pickedDoor = newPick;
  } else {
    stats.totalStayPlays++;
  }

  if (autoMode) {
    select('#instruction > p').html(hasSwitched ? 'Switch!' : 'Stay!');
    timeoutId = setTimeout(() => checkWin(hasSwitched), getDelayValue());
  } else {
    checkWin(hasSwitched);
  }
}
function revealDoor() {
  const options = doors.filter(
    (door, i) => i !== pickedDoor.index && door.prize !== carImage
  );

  // The player picked the right door
  if (options.length === doors.length - 1) {
    // Randomly remove one door from options
    options.splice(Math.floor(Math.random() * options.length), 1);
  }

  for (const revealedDoor of options) {
    revealedDoor.addClass('revealed');
    select('.content', revealedDoor).html(`<img src="${revealedDoor.prize}">`);
  }

  const lastDoor = doors.find(
    (door) => !door.hasClass('revealed') && !door.hasClass('picked')
  );
  
  select('#instruction > p').html(
    `The host opened door ${options[0].index + 1}! Do you want to switch to door #${lastDoor.index + 1}?`
  );

  if (autoMode) {
    if (Math.random() < 0.5) {
      timeoutId = setTimeout(() => chooseDoor(true), getDelayValue());
    } else {
      timeoutId = setTimeout(() => chooseDoor(false), getDelayValue());
    }
  } else {
    select('#instruction > .choices').show();
  }
}
function pickDoor() {
  if (state !== 'PICK') return;
  state = 'REVEAL';
  if (autoMode) {
    pickedDoor = random(doors);
  } else {
    pickedDoor = this;
  }
  pickedDoor.addClass('picked');
  if (autoMode) {
    setTimeout(revealDoor, getDelayValue());
  } else {
    revealDoor();
  }
}

function makeDoors() {
  // Clear existing doors
  for (let door of doors) {
    door.remove();
  }
  doors.splice(0, doors.length);

  for (let i = 0; i < totalDoors; i++) {
    doors[i] = createDiv();
    doors[i].parent('#doors');
    doors[i].class('door-container');
    if (totalDoors > 10) {
      doors[i].addClass('small');
    }
    doors[i].index = i;
    doors[i].mousePressed(pickDoor);

    const door = createDiv();
    door.class('door');
    door.parent(doors[i]);

    const content = createDiv();
    content.class('content');
    content.parent(doors[i]);
  }
}

function setup() {
  noCanvas();
  stats = getItem('montey-hall-stats') || stats;
  updateStats();
  makeDoors();
  reset();

  select('#nb-doors').changed(function () {
    totalDoors = +this.value();
    makeDoors();
    reset();
    clearStats();
  });

  select('button#yes').mousePressed(function () {
    chooseDoor(true);
  });

  select('button#no').mousePressed(function () {
    chooseDoor(false);
  });

  select('button#play-again').mousePressed(function () {
    reset();
  });

  select('button#autorun').mousePressed(function () {
    autoMode = !autoMode;
    if (autoMode) {
      this.addClass('on');
      reset();
      pickDoor();
      select('#speed-slider').show();
    } else {
      clearTimeout(timeoutId);
      this.removeClass('on');
      select('#speed-slider').hide();
      reset();
    }
  });
  select('#speed-slider').hide();
}

