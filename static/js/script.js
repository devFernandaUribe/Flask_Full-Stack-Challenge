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
  }

  async load() {
    const articles = await this.fetchPage();
    const wireframes = document.querySelectorAll(`.feed-${this.name} .feed-item`);
    wireframes.forEach((element, index) => {
      const data = articles[index];
      if (data) {
        let article = new Article(data);
        element.innerHTML = article.html;
        element.classList.remove('wireframe');
      } else {
        element.classList.add('hidden');
      }
    });
  }

  async fetchPage() {
    let response = await fetch(`${this.url}?p=${this.page}`);
    return await response.json() || {};
  }
}

for (let feedName of ['latest', 'trending']) {
  const feed = new Feed(feedName);
  feed.load();
}

/*// TODO load data into "recommended" feed
// These recommendations should change as the user interacts with the feed
console.log('Recommended');
console.log(document.querySelectorAll('.feed-personalized .feed-item'));*/
