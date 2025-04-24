document.addEventListener('DOMContentLoaded', function() {
    // DOM elements
    const startWorkoutBtn = document.getElementById('start-workout');
    const resetSelectionBtn = document.getElementById('reset-selection');
    const pauseTimerBtn = document.getElementById('pause-timer');
    const resumeTimerBtn = document.getElementById('resume-timer');
    const stopTimerBtn = document.getElementById('stop-timer');
    const timerDisplay = document.getElementById('timer');
    const currentExerciseDisplay = document.getElementById('current-exercise');
    const exerciseImage = document.getElementById('exercise-image');
    const setInfoDisplay = document.getElementById('set-info');
    const progressBar = document.getElementById('progress-bar');
    const selectedList = document.getElementById('selected-list');
    
    // Timer variables
    let timer;
    let timeLeft = 0;
    let totalTime = 0;
    let isPaused = false;
    let currentSet = 0;
    let totalSets = 0;
    let currentExerciseIndex = 0;
    let selectedExercises = [];
    let isRestPeriod = false;
    let isSetRestPeriod = false;
    
    // Exercise settings
    let exerciseDuration = 30;
    let exerciseRest = 15;
    let setRest = 60;
    
    // Initialize the app
    init();
    
    function init() {
        loadSettings();
        updateSelectedExercisesList();
        
        document.querySelectorAll('.exercise-checkbox').forEach(checkbox => {
            checkbox.addEventListener('change', updateSelectedExercisesList);
        });
        
        startWorkoutBtn.addEventListener('click', startWorkout);
        resetSelectionBtn.addEventListener('click', resetSelection);
        pauseTimerBtn.addEventListener('click', pauseTimer);
        resumeTimerBtn.addEventListener('click', resumeTimer);
        stopTimerBtn.addEventListener('click', stopTimer);
        
        document.getElementById('exercise-duration').addEventListener('change', updateSettings);
        document.getElementById('exercise-rest').addEventListener('change', updateSettings);
        document.getElementById('set-rest').addEventListener('change', updateSettings);
        document.getElementById('num-sets').addEventListener('change', updateSettings);
        
        document.querySelectorAll('.tab-button').forEach(button => {
            button.addEventListener('click', function() {
                const tabName = this.getAttribute('onclick').match(/'(.*?)'/)[1];
                openTab(tabName, this);
            });
        });
    }
    
    function loadSettings() {
        exerciseDuration = parseInt(document.getElementById('exercise-duration').value) || 30;
        exerciseRest = parseInt(document.getElementById('exercise-rest').value) || 15;
        setRest = parseInt(document.getElementById('set-rest').value) || 60;
        totalSets = parseInt(document.getElementById('num-sets').value) || 3;
    }
    
    function updateSettings() {
        loadSettings();
    }
    
    function updateSelectedExercisesList() {
        selectedExercises = [];
        document.querySelectorAll('.exercise-checkbox:checked').forEach(checkbox => {
            selectedExercises.push(checkbox.value);
        });
        
        selectedList.innerHTML = '';
        if (selectedExercises.length === 0) {
            selectedList.innerHTML = '<p>No exercises selected</p>';
        } else {
            selectedExercises.forEach(exercise => {
                const item = document.createElement('div');
                item.className = 'selected-exercise-item';
                item.textContent = exercise;
                selectedList.appendChild(item);
            });
        }
    }
    
    function resetSelection() {
        document.querySelectorAll('.exercise-checkbox').forEach(checkbox => {
            checkbox.checked = false;
        });
        updateSelectedExercisesList();
    }
    
    function startWorkout() {
        if (selectedExercises.length === 0) {
            alert('Please select at least one exercise');
            return;
        }
        
        loadSettings();
        currentSet = 1;
        currentExerciseIndex = 0;
        isRestPeriod = false;
        isSetRestPeriod = false;
        
        startWorkoutBtn.disabled = true;
        resetSelectionBtn.disabled = true;
        pauseTimerBtn.disabled = false;
        stopTimerBtn.disabled = false;
        
        startExercise();
    }
    
    function startExercise() {
        isRestPeriod = false;
        const exerciseName = selectedExercises[currentExerciseIndex];
        currentExerciseDisplay.textContent = exerciseName;
        setInfoDisplay.textContent = `Set: ${currentSet}/${totalSets}`;
        
        // Set exercise image
        exerciseImage.src = `/exercise_image/${exerciseName.toLowerCase().replace(/ /g, '_')}.jpg`;
        exerciseImage.style.display = 'block';
        exerciseImage.onerror = function() {
            this.style.display = 'none';
        };
        
        timeLeft = exerciseDuration;
        totalTime = exerciseDuration;
        updateTimerDisplay();
        progressBar.style.width = '100%';
        progressBar.style.backgroundColor = '#2ecc71';
        
        document.getElementById('start-sound').play();
        clearInterval(timer);
        timer = setInterval(updateTimer, 1000);
    }
    
    function startRestPeriod() {
        isRestPeriod = true;
        currentExerciseDisplay.textContent = 'Rest';
        exerciseImage.style.display = 'none';
        timeLeft = exerciseRest;
        totalTime = exerciseRest;
        updateTimerDisplay();
        progressBar.style.width = '100%';
        progressBar.style.backgroundColor = '#3498db';
        
        document.getElementById('rest-sound').play();
        clearInterval(timer);
        timer = setInterval(updateTimer, 1000);
    }
    
    function startSetRestPeriod() {
        isSetRestPeriod = true;
        currentExerciseDisplay.textContent = 'Set Rest';
        exerciseImage.style.display = 'none';
        timeLeft = setRest;
        totalTime = setRest;
        updateTimerDisplay();
        progressBar.style.width = '100%';
        progressBar.style.backgroundColor = '#e74c3c';
        
        document.getElementById('rest-sound').play();
        clearInterval(timer);
        timer = setInterval(updateTimer, 1000);
    }
    
    function updateTimer() {
        if (isPaused) return;
        
        timeLeft--;
        updateTimerDisplay();
        
        const progress = (timeLeft / totalTime) * 100;
        progressBar.style.width = `${progress}%`;
        
        if (timeLeft === 5) {
            document.getElementById('process-sound').play();
        }
        
        if (timeLeft <= 0) {
            clearInterval(timer);
            
            if (isSetRestPeriod) {
                currentSet++;
                isSetRestPeriod = false;
                
                if (currentSet > totalSets) {
                    endWorkout();
                } else {
                    currentExerciseIndex = 0;
                    startExercise();
                }
            } else if (isRestPeriod) {
                isRestPeriod = false;
                currentExerciseIndex++;
                
                if (currentExerciseIndex >= selectedExercises.length) {
                    if (currentSet < totalSets) {
                        startSetRestPeriod();
                    } else {
                        endWorkout();
                    }
                } else {
                    startExercise();
                }
            } else {
                if (currentExerciseIndex < selectedExercises.length - 1) {
                    startRestPeriod();
                } else {
                    if (currentSet < totalSets) {
                        startSetRestPeriod();
                    } else {
                        endWorkout();
                    }
                }
            }
        }
    }
    
    function updateTimerDisplay() {
        const minutes = Math.floor(timeLeft / 60);
        const seconds = timeLeft % 60;
        timerDisplay.textContent = `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
    }
    
    function pauseTimer() {
        isPaused = true;
        pauseTimerBtn.disabled = true;
        resumeTimerBtn.disabled = false;
    }
    
    function resumeTimer() {
        isPaused = false;
        pauseTimerBtn.disabled = false;
        resumeTimerBtn.disabled = true;
    }
    
    function stopTimer() {
        clearInterval(timer);
        endWorkout();
    }
    
    function endWorkout() {
        timerDisplay.textContent = '00:00';
        currentExerciseDisplay.textContent = 'Workout Complete!';
        exerciseImage.style.display = 'none';
        setInfoDisplay.textContent = '';
        progressBar.style.width = '0%';
        
        document.getElementById('stop-sound').play();
        
        startWorkoutBtn.disabled = false;
        resetSelectionBtn.disabled = false;
        pauseTimerBtn.disabled = true;
        resumeTimerBtn.disabled = true;
        stopTimerBtn.disabled = true;
        
        currentSet = 0;
        currentExerciseIndex = 0;
        isRestPeriod = false;
        isSetRestPeriod = false;
    }
    
    function openTab(tabName, button) {
        const tabContents = document.getElementsByClassName('tab-content');
        for (let i = 0; i < tabContents.length; i++) {
            tabContents[i].style.display = 'none';
        }
        
        const tabButtons = document.getElementsByClassName('tab-button');
        for (let i = 0; i < tabButtons.length; i++) {
            tabButtons[i].classList.remove('active');
        }
        
        document.getElementById(tabName).style.display = 'block';
        button.classList.add('active');
    }
});