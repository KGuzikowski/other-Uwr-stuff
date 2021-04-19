// TASK 1 and 2:
// Code below should be copied and pasted into the mongo shell.

db.createCollection("books", {
    validator: {
        $jsonSchema: {
            bsonType: "object",
            required: ["title", "author", "is_copy", "available"],
            properties: {
                title: {
                    bsonType: "string",
                    description: "must be a string and is required"
                },
                author: {
                    bsonType: "string",
                    description: "must be a string and is required"
                },
                is_copy: {
                    bsonType: "bool",
                    description: "must be a boolean value and is required"
                },
                available: {
                    bsonType: "bool",
                    description: "must be a boolean value and is required"
                },
                borrowings: {
                    bsonType: "array",
                    items: {
                        bsonType: "object",
                        required: ["user_id", "start_date"],
                        properties: {
                            user_id: {
                                bsonType: "objectId",
                                description: "must be a objectId and is required"
                            },
                            start_date: {
                                bsonType: "date",
                                description: "must be a date and is required"
                            },
                            end_date: {
                                bsonType: "date",
                                description: "must be a date and is required"
                            }
                        }
                    },
                    description: "must be a array of objects and is required"
                }
            }
        }
    }
});

let user1 = ObjectId();
let user2 = ObjectId();

db.books.insertMany([
{
    title: "Hobbit",
    author: "J.R.R. Tolkien",
    is_copy: false,
    available: false,
    borrowings: [
        {
            user_id: user1,
            start_date: new Date(2018, 11, 24, 10, 33),
            end_date: new Date(2018, 11, 26, 10, 33),
        },
        {
            user_id: user2,
            start_date: new Date(2021, 04, 17, 10, 33)
        }
    ]
},
{
    title: "Hobbit",
    author: "J.R.R. Tolkien",
    is_copy: true,
    available: true
},
{
    title: "The Lord of the Rings",
    author: "J.R.R. Tolkien",
    is_copy: false,
    available: false,
    borrowings: [
        {
            user_id: user2,
            start_date: new Date(2018, 11, 26, 10, 33),
            end_date: new Date(2018, 12, 2, 10, 33),
        },
        {
            user_id: user1,
            start_date: new Date(2021, 04, 17, 10, 33)
        }
    ]
},
{
    title: "The Lord of the Rings",
    author: "J.R.R. Tolkien",
    is_copy: true,
    available: true
},
{
    title: "Silmarillion",
    author: "J.R.R. Tolkien",
    is_copy: true,
    available: true
}
]);

// 1. use db.books.find().pretty() to list the results

// TASK 3:

// a) Get full documents list, sorted in an explicit order,
//    and limited to the middle 2 items (select a specific page).
// Solution:
// db.books.find().sort({ title: 1 }).skip(2).limit(2).pretty()

// b) Get the documents list filtered with some
//    condition applied on the nested structure.
// Solution:
// db.books.find({ "borrowings.end_date": { $exists: true } } ).pretty()