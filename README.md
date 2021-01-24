# place-review-system
An overhaul of the current review system, enabling useful feedback through datapoints for hospitality venues 

## TODO:
- User testing
- Review form
  -> Add feedback model to review admin page
  -> Post operation validation
  -> Needs a seperate html page from detail (or extend differently), as it will handle errors differently
- Review testing
- Scorecard
  -> constraints
  -> delete related record
  -> update function
- Scorecard testing
- Details view to display scorecard
- View testing
- Move away from w3.css and implement custom sass for UI

## Considerations"
- Consider what data to keep when users/reviews/venues are deleted
- Crossovers in place attributes?
  -> Food/Drink and Quality
- Refactor review.html to remove repetition, need to reference and loop through Feedback model field names
