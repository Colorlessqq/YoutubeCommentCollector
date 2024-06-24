# YouTube Comments Extractor

This application helps YouTubers gather comments from their videos for various reasons, such as giveaways, gaining insights from followers, and more. The app offers several options to filter and save comments according to your needs.

#### Video Demo:  [https://www.youtube.com/watch?v=ARHlPxVeTGg&ab_channel=Ahmet](https://www.youtube.com/watch?v=ARHlPxVeTGg&ab_channel=Ahmet) (My English wasn't at its best while I was recording this)

## Features

1. **Filter Comments by Likes:** 
   - Choose to extract comments that have a minimum number of likes (e.g., at least 100 likes).

2. **Filter Comments by Text:**
   - Specify text that comments must include (e.g., comments containing "Hello").

3. **Error Handling:**
   - Invalid Links: The app will reject links that are not from YouTube.
   - Save Errors: The app will notify you of how many comments were not saved due to errors.

4. **Save Options:**
   - Save Comments Only: Save only the text of the comments.
   - Save Comments with Details: Save the comment text, username, and the number of likes.
   - Save as Screenshots: Save all comments as screenshots.

## Technology Stack

- **PyQt5:** Used to create the visual interface of the application.
- **Selenium:** Used to retrieve comments from the given YouTube link.

## Usage

1. **Input YouTube Link:** Enter the YouTube video link from which you want to extract comments.
2. **Set Filters:** Choose the filters based on likes and specific text content.
3. **Select Save Options:** Decide how you want to save the comments (text only, with details, or as screenshots).
4. **Run Extraction:** The app will process the comments and save them according to your selected options.

## Error Handling

- The app ensures that only valid YouTube links are processed.
- If there are errors while saving comments, the app will inform you about the number of comments that could not be saved.

This project is designed to simplify the process of extracting and saving YouTube comments, making it easier for content creators to manage their audience interactions.
