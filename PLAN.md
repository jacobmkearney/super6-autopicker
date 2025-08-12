1. **Add Command Line Argument:**
   - Introduce a new command line argument `optimise` in `client.py`.

2. **Read Predictions:**
   - Load the predicted scores from `data/score_predictions.json`.

3. **Navigate to Website:**
   - Open `https://super6.skysports.com/play`.
   - Handle redirection to `https://super6.skysports.com/played` if predictions are already submitted.

4. **Edit Predictions:**
   - If redirected, locate and click the `Edit` button:
     ```html
     <button font-size="large" id="js-fixtures-edit-entry" data-test-id="show-predictions-edit-button" class="css-1786ade e1d5c1xv9">Edit</button>
     ```

5. **Adjust Scores:**
   - Iterate through each match container:
     ```html
     <div data-test-id="match-container-1" class="css-1ks4pa3 e1y7qo030">
       <!-- Match details and score controls -->
     </div>
     ```
   - Compare current scores with those in `score_predictions.json`.
   - Adjust scores using the decrease button if necessary:
     ```html
     <button tabindex="-1" id="decrease-score-84978-team-home" data-test-id="match-team-prediction-home-decrease" class="css-x98jgc e1y7qo037"></button>
     <button tabindex="-1" id="decrease-score-84978-team-away" data-test-id="match-team-prediction-away-decrease" class="css-x98jgc e1y7qo037"></button>
     ```

6. **Submit Predictions:**
   - After adjusting all scores, submit the updated predictions.
