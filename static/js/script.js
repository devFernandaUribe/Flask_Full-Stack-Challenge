class Article {
  constructor(data) {
    this.data = this.normalizeData(data);
    this.html = this.toHTML();
  }

  normalizeData(data) {
    const { category, name, canonical_path, last_updated, created_at, thumbnails, type } = data || {};
    return {
      category: category || type,
      href: `/article${canonical_path}`,
      image: this.getImage(thumbnails),
      name,
      published: new Date(last_updated || created_at).toLocaleDateString('en-us'),
    };
  }

  getImage(thumbnails) {
    if (thumbnails) {
      thumbnails = thumbnails[0]?.sizes || [];
      return thumbnails.find(k => k.size === 'standard')?.url;
    }
    return '';
  }

  toHTML() {
    const { href, image, category, published, name } = this.data;
    return `
      <div class="thumbnail-wrapper">
        <a href="${href}">
          <img alt="" src="${image}" />
        </a>
      </div>
      <div class="text-wrapper">
        <p>
          <span class="category">${category}</span>
          •
          <span class="published">${published}</span>
        </p>
        <a href="/article${href}">
          <h2>${name}</h2>
        </a>
      </div>
    `;
  }
}

class Feed {
  constructor(name) {
    this.name = name;
    this.url = `/api/${name}`;
    this.page = 1;

    // set up "Load More" button
    this.moreButton = document.querySelector(`.feed-${this.name} .button-more`);
    if (this.moreButton) {
      this.moreButton.onclick = () => this.more();
    }
  }

  async load() {
    const articles = await this.fetchPage();
    const wireframes = document.querySelectorAll(`.feed-${this.name} .feed-item`);
    wireframes.forEach((element, index) => {
      const data = articles[index];
      if (data) {
        const article = new Article(data);
        element.innerHTML = article.html;
        element.classList.remove('wireframe');
      } else {
        element.classList.add('hidden');
        this.moreButton.classList.add('hidden');
      }
    });
  }

  async more() {
    this.moreButton.classList.add('hidden');
    this.page += 1;
    const articles = await this.fetchPage();
    if (articles?.length) {
      let elemToCopy = document.querySelector(`.feed-${this.name} .feed-item`);
      for (const data of articles) {
        const article = new Article(data);
        const clone = elemToCopy.cloneNode(true);
        clone.innerHTML = article.html;
        document.querySelector(`.feed-${this.name} .feed`).appendChild(clone);
        elemToCopy = clone;
      }
      this.moreButton.classList.remove('hidden');
    }
  }

  async fetchPage() {
    let response = await fetch(`${this.url}?p=${this.page}`);
    return await response.json() || [];
  }
}

class Page {
  constructor() {
    this.feeds = {
      latest: null,
      trending: null,
    };
  }

  render() {
    // load each of the feeds in the page
    for (let feedName of Object.keys(this.feeds)) {
      const feed = new Feed(feedName);
      feed.load();
      this.feeds[feedName] = feed;
    }
  }
}

const page = new Page();
page.render();

/*// TODO load data into "recommended" feed
// These recommendations should change as the user interacts with the feed
console.log('Recommended');
console.log(document.querySelectorAll('.feed-personalized .feed-item'));*/
