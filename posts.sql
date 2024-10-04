IF OBJECT_ID('Post', 'U') IS NOT NULL
    DROP TABLE [Post];
    
IF OBJECT_ID('Comment', 'U') IS NOT NULL
    DROP TABLE Comment;

IF OBJECT_ID('Tag', 'U') IS NOT NULL
    DROP TABLE [Tag];

IF OBJECT_ID('User', 'U') IS NOT NULL
    DROP TABLE [User];

-- Create User Table
CREATE TABLE [User] (
    UserId INTEGER,
    Username NVARCHAR(50) NOT NULL,
    CONSTRAINT PK_User PRIMARY KEY (UserId)
);

-- Create Tag Table
CREATE TABLE [Tag] (
    TagId INTEGER,
    TagName NVARCHAR(50) NOT NULL,
    CONSTRAINT PK_Tag PRIMARY KEY (TagId)
);

-- Create Post Table
CREATE TABLE [Post] (
    PostId INTEGER,
    PostText NVARCHAR(50) NOT NULL,
    Draft BIT,
    UserId INTEGER NOT NULL,
    CONSTRAINT PK_Post PRIMARY KEY (PostId),
    CONSTRAINT FK_Post_User FOREIGN KEY (UserId) REFERENCES [User](UserId) ON DELETE CASCADE
);

-- Join table for Posts and Tags (many-to-many relationship)
CREATE TABLE PostTags (
    PostId INTEGER NOT NULL,
    TagId INTEGER NOT NULL,
    CONSTRAINT FK_PostTags_Post FOREIGN KEY (PostId) REFERENCES Post(PostId) ON DELETE CASCADE,
    CONSTRAINT FK_PostTags_Tag FOREIGN KEY (TagId) REFERENCES Tag(TagId) ON DELETE CASCADE
);

-- Create Comment Table
CREATE TABLE Comment (
    CommentId INTEGER NOT NULL,
    CommentText NVARCHAR(50),
    PostId INTEGER NOT NULL,
    UserId INTEGER NOT NULL,
    CONSTRAINT PK_Comment PRIMARY KEY (CommentId),
    CONSTRAINT FK_Comment_Post FOREIGN KEY (PostId) REFERENCES Post(PostId) ON DELETE CASCADE,
    CONSTRAINT FK_Comment_User FOREIGN KEY (UserId) REFERENCES [User](UserId) ON DELETE CASCADE
);



-- SQL Queries

--Query for Draft Posts:
SELECT PostId, PostText, UserId  FROM Post WHERE Draft = 1;

--Query for Post by ID with Comments:
SELECT p.PostId, p.PostText, p.UserId, c.CommentId, c.CommentText 
FROM Post p 
LEFT JOIN Comment c ON p.PostId = c.PostId
WHERE p.PostId = 'post-id';

--Query for User by ID with Posts and Comments:
SELECT u.UserId, u.Username, p.PostId, p.PostText, c.CommentId, c.CommentText 
FROM [User] u
LEFT JOIN Post p ON u.UserId = p.UserId
LEFT JOIN Comment c ON p.PostId = c.PostId
WHERE u.UserId = 'user-id';



