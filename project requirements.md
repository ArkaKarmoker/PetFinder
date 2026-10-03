# Pet Adoption & Rescue Platform

🎯 **Project Overview**

Build a web application where users can browse pets available for adoption and submit adoption requests.

There will be **three main parts**:

1.  Pet management
2.  User adoption requests
3.  Admin management

Students should build both:

*   **Django Template-based website**
*   **REST API using Django REST Framework**

---

## 1. 👤 User Features

Users should be able to:

### Authentication

*   Register
*   Login
*   Logout
*   View their profile

### Pet Browsing

Users can see:

*   Pet name
*   Pet image
*   Animal type
*   Breed
*   Age
*   Gender
*   Location
*   Description
*   Adoption status

Example:

🐕 Max

Type: Dog  
Breed: Golden Retriever  
Age: 2 years  
Gender: Male  
Location: Dhaka

Status: Available

---

## 2. 🔍 Search & Filter Pets

Users should be able to search/filter pets by:

*   Pet name
*   Animal type
*   Breed
*   Gender
*   Location
*   Adoption status

Example:

Search: Dog

Gender: Male  
Location: Dhaka

The result should show matching pets.

---

## 3. 🐾 Pet Details

Create a separate pet details page.

For example:

-----------------------
🐕 MAX
-----------------------

[    Pet Image    ]

Name: Max  
Type: Dog  
Breed: Golden Retriever  
Age: 2 years  
Gender: Male  
Location: Dhaka

About Max:
Max is friendly and playful...

Status: Available

[ Apply for Adoption ]

If the pet has already been adopted:

❌ This pet has already been adopted.

The adoption button should not be available.

---

## 4. ❤️ Adoption Request

A logged-in user can apply to adopt an available pet.

The user submits:

*   Address
*   Phone number
*   Reason for adoption
*   Previous pet experience
*   Optional message

Example:

Adoption Application

Address: __________________

Phone: ____________________

Why do you want this pet?
__________________________

Have you owned a pet before?
Yes / No

Additional message:
__________________________

[ Submit Application ]

---

## 5. 📋 My Adoption Requests

Users should have a dashboard where they can see their applications.

Example:

| Pet | Date | Status |
| :--- | :--- | :--- |
| Max | 20 Sep | Pending |
| Luna | 18 Sep | Rejected |
| Coco | 15 Sep | Approved |

Possible statuses:

Pending  
Approved  
Rejected  

---

## 6. 🔧 Django Admin

The admin should be used to manage the entire system.

Admin should be able to:

### Manage Pets

*   Add pet
*   Edit pet
*   Delete pet
*   Change adoption status
*   Upload pet image

### Manage Adoption Requests

Admin can see:

User  
Pet  
Application Date  
Phone  
Reason  
Status  

Admin can change:

Pending → Approved  
Pending → Rejected

---

## 7. 🧠 Important Business Logic

This is where the assignment becomes more than simple CRUD.

### Rule 1 — Only available pets can be adopted

If:

Pet status = Adopted

the user cannot submit a new application.

---

### Rule 2 — One user cannot submit multiple active requests for the same pet

For example:

User: Rahim  
Pet: Max  
Status: Pending  

Rahim shouldn't be able to submit another application for Max.

---

### Rule 3 — Approved application

When admin approves an application:

Adoption Request  
↓  
Approved  
↓  
Pet Status = Adopted

And other pending requests for that same pet should no longer be accepted.

Students don't need to implement complicated automatic cancellation if you want to keep the project easier; they can simply prevent further applications.

---

## 8. 🌐 REST API

Students must create APIs using **Django REST Framework**.

### Pet API

GET /api/pets/  
GET /api/pets/&lt;id&gt;/  
POST /api/pets/  
PUT /api/pets/&lt;id&gt;/  
DELETE /api/pets/&lt;id&gt;/  

You can require authentication/permission for creating, updating and deleting pets.

---

### Adoption API

GET /api/adoptions/  
POST /api/adoptions/  
GET /api/adoptions/&lt;id&gt;/  
PUT /api/adoptions/&lt;id&gt;/  

Users should only be able to access their own adoption requests through the API.

---

### Search API

Example:

GET /api/pets/?search=golden  

And filtering:

GET /api/pets/?animal_type=Dog  
GET /api/pets/?gender=Male  

---

## 9. 🗃️ Suggested Models

Students can design their own models, but they should have at least:

### Pet

Pet
--------------
name  
animal_type  
breed  
age  
gender  
location  
description  
image  
status  
created_at  

### AdoptionRequest

AdoptionRequest
--------------
user  
pet  
phone  
address  
reason  
previous_pet_experience  
message  
status  
created_at  

They should use Django's built-in `User` model.

---

## 10. 🔗 Relationship

The main relationship should be:

```text
User
|
|_________________
        ↓
   AdoptionRequest
        ↑
        |
       Pet
```

One user can submit multiple adoption requests.

One pet can receive multiple adoption requests.

---

## 11. 🖥️ Required Pages

Students should create at least these pages:

```text
Home
|
├── Pet List
|
├── Pet Details
|
├── Login
|
├── Register
|
├── User Dashboard
|   └── My Adoption Requests
|
└── Adoption Form
```

They don't need to build a separate custom admin dashboard because **Django Admin** will be used for administration.

---

## 12. 🎨 UI Requirements

The UI doesn't need to be highly professional.

But it should have:

*   Navigation bar
*   Pet cards
*   Search/filter form
*   Responsive layout
*   Login/register forms
*   Adoption form
*   User dashboard
*   Success/error messages

Students can use **Bootstrap** if they want.

---

## 13. ⭐ Bonus Features

These are optional and can give extra marks.

### ⭐ Favorite Pets

Users can save pets to favorites.

❤️ Add to Favorites

### ⭐ Pagination

Show:

1 2 3 Next

### ⭐ API Pagination

Example:

/api/pets/?page=2

### ⭐ API Authentication

Implement:

Token Authentication

or another authentication method taught in class.

### ⭐ Pet Categories

Examples:

Dog
Cat
Bird
Rabbit
Other

---

## 📦 Submission Requirements

Students must submit:

1.  **GitHub repository URL**
2.  `README.md`
3.  `requirements.txt`
4.  Database migrations