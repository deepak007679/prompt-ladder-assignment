# Run 0: Baseline (The Lazy Prompt)

## 📌 Prompt
```text
Write backend code
```

---

## 💻 Full Representative Output
```javascript
// Here is a simple backend server using Node.js and Express:
const express = require('express');
const app = express();
const PORT = 3000;

app.use(express.json());

// In-memory data store
let items = [
  { id: 1, name: 'Item One', description: 'This is the first item' },
  { id: 2, name: 'Item Two', description: 'This is the second item' }
];

// GET /api/items - Retrieve all items
app.get('/api/items', (req, res) => {
  res.status(200).json(items);
});

// GET /api/items/:id - Retrieve a single item by ID
app.get('/api/items/:id', (req, res) => {
  const item = items.find(i => i.id === parseInt(req.params.id));
  if (!item) return res.status(404).json({ error: 'Item not found' });
  res.status(200).json(item);
});

// POST /api/items - Create a new item
app.post('/api/items', (req, res) => {
  const newItem = {
    id: items.length + 1,
    name: req.body.name,
    description: req.body.description
  };
  items.push(newItem);
  res.status(201).json(newItem);
});

app.listen(PORT, () => {
  console.log(`Backend server running on http://localhost:${PORT}`);
});
```

### Explanatory Prose Provided by the Model:
> "Backend code manages data storage, business logic, and API endpoints. In the example above, we use Express.js to create REST endpoints.
> - **GET** retrieves data from the server.
> - **POST** submits new data to be processed and stored.
> 
> To build a more complete backend, please clarify:
> 1. What programming language or runtime do you prefer (Python, Node.js, Go, Java)?
> 2. What database will you be using (PostgreSQL, MongoDB, MySQL)?
> 3. What is the business domain (e.g., e-commerce, authentication, blogging)?
> 4. Do you need user authentication and session management?
> 5. How should data validation be handled?
> 6. What hosting or cloud infrastructure are you targeting?"

---

## 🔍 Four Mandatory Analysis Notes

1. **What changed in the prompt:**  
   Nothing. This is the baseline lazy prompt typed without specificity, context, or direction.
2. **What actually improved in the output:**  
   Baseline evaluation. No improvements.
3. **What still failed:**  
   The output is completely non-actionable for real engineering. It guessed an arbitrary language (Node.js/JavaScript), invented a toy domain ("items" array) stored in volatile memory, explained basic HTTP verbs suitable only for absolute beginners, and asked 6+ scoping questions.
4. **What I would try next:**  
   Add **a clearer goal** specifying the exact business and technical feature required: user authentication, password resets, and session token generation for a SaaS application.
