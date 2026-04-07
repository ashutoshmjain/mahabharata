# How to Turn Your mdBook into a High-Performance Mobile App (PWA)

If you use **mdBook** to write documentation, books, or notes, you already know it’s great for the web. But what if you could "install" your book on your phone or desktop, have a cool icon on your home screen, and—most importantly—**read it entirely offline** (like on a plane)?

This is called a **Progressive Web App (PWA)**. In this guide, I’ll walk you through how we turned the *Mahabharata* digitization project into a professional-grade app, the "gotchas" we hit, and how you can do it too.

---

### 1. The Ingredients
To make this work, we need three things:
1.  **`manifest.json`**: The "ID card" that tells the browser "I am an app."
2.  **Workbox**: A tool from Google that handles the "Service Worker" (the brain that saves files for offline use).
3.  **A Custom Theme**: To tell mdBook to load our app scripts.

---

### 2. Step-by-Step Walkthrough

#### Step A: Generating the Icons (The "Magic" Way)
A PWA needs an icon. But it can't just be any image; it needs to be square, and modern Android/iOS devices require a "safe zone" so they can crop your icon into different shapes (circles, squares, squircycles).

We used a tool called **ImageMagick**. If you have an SVG logo (like `logo.svg`), run these commands to create perfect, professional icons:

```bash
# Create a large icon (512px) with a dark background and a "safe zone"
convert logo.svg -resize 400x400 -background "#2e2e2e" -gravity center -extent 512x512 icon-512x512.png

# Create a smaller version (192px)
convert logo.svg -resize 150x150 -background "#2e2e2e" -gravity center -extent 192x192 icon-192x192.png
```
*Note: We resized the logo to be slightly smaller (400px) than the canvas (512px). This creates a "Safe Zone" so your logo doesn't get cut off when the phone rounds the corners!*

#### Step B: The App "ID Card" (`manifest.json`)
Create a file named `pwa/manifest.json`. This tells the phone what color the top bar should be and what the app is called:

```json
{
  "id": "my-book-pwa",
  "name": "My Great Book",
  "display": "standalone",
  "start_url": "index.html",
  "background_color": "#2e2e2e",
  "theme_color": "#2e2e2e",
  "icons": [
    { "src": "icons/icon-512x512.png", "sizes": "512x512", "type": "image/png", "purpose": "any maskable" }
  ]
}
```

#### Step C: The Offline "Brain" (Workbox)
We use a file called `sw-src.js`. Its only job is to say: "Save every single page of this book into the phone's memory."

```javascript
import { precacheAndRoute } from 'workbox-precaching';
// This line is magic; Workbox fills it with your file list later
precacheAndRoute(self.__WB_MANIFEST);
```

---

### 3. The Bugs We Found (And How to Fix Them)

When we first tried this, the "Install" button wouldn't show up. Here are the three "Boss Fights" we won:

#### Bug 1: The "Fleeting" Install Button
**Problem:** You see the install icon for a split second, then it vanishes.
**The Fix:** Chrome requires a Service Worker to have a "fetch handler." We had to update our script to explicitly handle navigation requests so Chrome was 100% sure the app worked offline.

#### Bug 2: Deep Links
**Problem:** If you are reading `Chapter 5` (a nested folder), the app couldn't find the `manifest.json` because it was looking in the wrong folder.
**The Fix:** We used mdBook’s `{{ path_to_root }}` variable in the HTML head. This ensures that no matter how deep you are in the book, the app always knows where its "ID card" is.

#### Bug 3: The "Wait, Where Was I?" Problem
**Problem:** If you close the app and reopen it, it always starts at the cover page.
**The Fix:** We wrote a "Persistence Script." Every time you read a page, the app saves that URL. When you reopen the app, it instantly teleports you back to the last paragraph you were reading.

---

### 4. How to Test It Locally

You can't test a PWA just by double-clicking an HTML file. You need a "Server."

1.  **Build your book**: `mdbook build`
2.  **Run a local server**: 
    ```bash
    # If you have Node.js installed:
    npx serve book
    ```
3.  **Open Chrome**: Go to `http://localhost:3000`.
4.  **Look for the Icon**: In the address bar (near the "Star/Bookmark" icon), you should see a small computer icon with an arrow pointing down. **That is your Install button!**

---

### 5. What to Expect After Installing
Once you click Install:
*   The browser "frame" disappears. It looks like a real app.
*   You get a shortcut on your Desktop or Phone Home Screen.
*   **The Ultimate Test**: Turn off your Wifi. Refresh the page. If the book still loads, you’ve successfully built an offline-first PWA!

---

### 6. Automating the Build with GitHub Actions

You don't want to manually run `npm run build:pwa` and upload files every time you write a new chapter. We use **GitHub Actions** to do this automatically. Every time you `git push`, GitHub starts a "Robot" (a Virtual Machine) that builds your book and publishes it to **GitHub Pages**.

#### The "Magic" Workflow File
Create a file at `.github/workflows/mdbook.yml`. Here is the exact setup we used for the *Mahabharata* project:

```yaml
name: Deploy PWA to GitHub Pages

on:
  push:
    branches: ["main"] # Only run when we push to the main branch

permissions:
  contents: read
  pages: write
  id-token: write

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      # 1. Install mdBook (The Book Generator)
      - name: Install mdbook
        run: |
          mkdir mdbook
          curl -sSL https://github.com/rust-lang/mdBook/releases/download/v0.4.37/mdbook-v0.4.37-x86_64-unknown-linux-gnu.tar.gz | tar -xzC ./mdbook
          echo "$(pwd)/mdbook" >> $GITHUB_PATH

      # 2. Setup Node.js (The PWA Generator)
      - name: Setup Node
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'

      - name: Install dependencies
        run: npm install

      # 3. The "Big Build"
      # This runs our custom script that builds the book AND injects the PWA brain
      - name: Build with PWA assets
        run: npm run build:pwa

      # 4. Upload and Deploy to the Internet
      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: './book' # Upload the "book" folder we just built

      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
```

#### Why This is Important for PWAs:
1.  **Workbox Revisioning**: Every time this "Robot" runs, it gives each of your chapters a unique ID (like a fingerprint). If you change just one sentence in Chapter 2, Workbox knows *only* that file changed.
2.  **Background Updates**: When your readers open the app, it checks if a new version was built on GitHub. If it finds one, it downloads the new chapters in the background while they read.
3.  **No Manual Errors**: You never have to worry about forgetting to copy the `manifest.json` or `sw.js` files. The robot does it perfectly every time.

#### How to Enable It:
1.  Push this file to your GitHub repository.
2.  Go to your repository **Settings** -> **Pages**.
3.  Under **Build and deployment**, change the "Source" to **GitHub Actions**.

#### What to Expect:
Next time you push your code, go to the **Actions** tab in GitHub. You’ll see a yellow spinning circle. When it turns into a green checkmark, your book is live! 

If you already have the app installed on your phone, just open it. Within a few seconds, it will silently update itself to the latest version you just pushed!
