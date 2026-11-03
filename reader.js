(function () {
  'use strict';

  var article = document.getElementById('reader-story');
  var heading = document.getElementById('reader-title');
  var status = document.getElementById('reader-status');
  var content = document.getElementById('reader-content');
  var retry = document.getElementById('reader-retry');
  var storyId = new URLSearchParams(location.search).get('story');

  function closeWindow() {
    try { window.close(); } catch (error) { /* The browser may require its own close control. */ }
    setTimeout(function () {
      var note = document.getElementById('reader-close-status');
      note.textContent = 'If this window remains open, close it using your browser.';
      note.hidden = false;
    }, 150);
  }

  document.getElementById('reader-close').addEventListener('click', closeWindow);
  document.addEventListener('keydown', function (event) {
    if (event.key === 'Escape') closeWindow();
  });

  // Only exact, known YouTube video hosts and eleven-character video IDs
  // become players. Channels, lookalike domains and arbitrary URLs remain links.
  function youtubeVideo(href) {
    var url;
    try { url = new URL(href, location.href); } catch (error) { return null; }
    if (url.protocol !== 'https:' || url.username || url.password || url.port) return null;
    var id;
    if (url.hostname === 'youtu.be') {
      var shortPath = url.pathname.match(/^\/([A-Za-z0-9_-]{11})$/);
      id = shortPath ? shortPath[1] : null;
    } else if (['youtube.com', 'www.youtube.com', 'm.youtube.com'].indexOf(url.hostname) !== -1 && url.pathname === '/watch') {
      id = url.searchParams.get('v');
    }
    if (!id || !/^[A-Za-z0-9_-]{11}$/.test(id)) return null;

    var rawTime = url.searchParams.get('start') || url.searchParams.get('t') || new URLSearchParams(url.hash.slice(1)).get('t') || '';
    var start = 0;
    if (/^\d+$/.test(rawTime)) start = Number(rawTime);
    else {
      var timeParts = rawTime.match(/^(?:(\d+)h)?(?:(\d+)m)?(?:(\d+)s)?$/);
      if (rawTime && timeParts) start = Number(timeParts[1] || 0) * 3600 + Number(timeParts[2] || 0) * 60 + Number(timeParts[3] || 0);
    }
    return { id: id, start: Number.isSafeInteger(start) && start > 0 ? start : 0 };
  }

  function cloneContent(element) {
    var clone = element.cloneNode(true);
    // Imported article markup is content; it must not run page behaviours.
    clone.querySelectorAll('script, style, iframe, object, embed').forEach(function (node) { node.remove(); });
    [clone].concat(Array.from(clone.querySelectorAll('*'))).forEach(function (node) {
      Array.from(node.attributes).forEach(function (attribute) {
        if (/^on/i.test(attribute.name)) node.removeAttribute(attribute.name);
      });
    });
    var links = Array.from(clone.querySelectorAll('a'));
    if (clone.matches('a')) links.unshift(clone);
    links.forEach(function (link) {
      link.target = '_blank';
      link.rel = 'noopener noreferrer';
      link.setAttribute('aria-description', 'Opens in a new tab');
      var destination;
      try { destination = new URL(link.getAttribute('href'), location.href); } catch (error) { return; }
      if (['http:', 'https:', 'mailto:', 'tel:'].indexOf(destination.protocol) === -1) link.removeAttribute('href');
    });
    var images = Array.from(clone.querySelectorAll('img'));
    if (clone.matches('img')) images.unshift(clone);
    images.forEach(function (image) { image.loading = 'lazy'; });
    return clone;
  }

  function renderStory(story) {
    var sourceHeading = story.querySelector('h3');
    if (!sourceHeading) throw new Error('The selected story is incomplete.');
    var title = sourceHeading.textContent.trim();
    heading.textContent = title;
    document.title = title + ' — Math Together Canada';
    content.replaceChildren();

    var date = story.querySelector(':scope > .date');
    if (date) {
      var displayedDate = cloneContent(date);
      displayedDate.className = 'reader-date';
      content.appendChild(displayedDate);
    }

    var body = document.createElement('div');
    body.className = 'reader-body';
    var details = story.querySelector(':scope > details');
    if (details) {
      Array.from(details.children).forEach(function (node) {
        if (!node.matches('summary, script, style, iframe, object, embed')) body.appendChild(cloneContent(node));
      });
    } else {
      Array.from(story.children).forEach(function (node) {
        if ((node.tagName === 'P' && !node.matches('.date, .story-preview')) || node.matches('.story-video-links')) body.appendChild(cloneContent(node));
      });
    }

    var videos = [];
    var seen = new Set();
    body.querySelectorAll('a[href]').forEach(function (link) {
      var video = youtubeVideo(link.getAttribute('href'));
      if (!video || seen.has(video.id)) return;
      seen.add(video.id);
      video.label = link.textContent.trim() || title;
      videos.push(video);
    });

    // For a video-only entry, the player is the content rather than a second
    // copy of its poster. Written stories retain their original cover image.
    var sourceImage = story.querySelector('.news-image img');
    if (sourceImage && (details || videos.length === 0)) {
      var cover = cloneContent(sourceImage);
      cover.classList.add('reader-cover');
      cover.loading = 'eager';
      content.appendChild(cover);
    }

    if (videos.length) {
      var players = document.createElement('div');
      players.className = 'reader-videos';
      videos.forEach(function (video) {
        var figure = document.createElement('figure');
        figure.className = 'reader-video';
        var player = document.createElement('iframe');
        player.src = 'https://www.youtube-nocookie.com/embed/' + video.id + (video.start ? '?start=' + video.start : '');
        player.title = title + ' — ' + video.label;
        player.loading = 'lazy';
        player.allow = 'accelerometer; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share';
        player.allowFullscreen = true;
        player.referrerPolicy = 'strict-origin-when-cross-origin';
        figure.appendChild(player);
        var caption = document.createElement('figcaption');
        caption.textContent = video.label;
        figure.appendChild(caption);
        players.appendChild(figure);
      });
      content.appendChild(players);
    }
    content.appendChild(body);
    status.hidden = true;
    retry.hidden = true;
    article.setAttribute('aria-busy', 'false');
    heading.focus({ preventScroll: true });
  }

  function loadStory() {
    article.setAttribute('aria-busy', 'true');
    heading.textContent = 'Loading story…';
    status.textContent = 'Loading the selected story.';
    status.hidden = false;
    retry.hidden = true;
    content.replaceChildren();
    if (!storyId) {
      showError('No story was selected.');
      return;
    }
    fetch('news.html', { cache: 'no-cache' }).then(function (response) {
      if (!response.ok) throw new Error('The story could not be loaded. Please try again.');
      return response.text();
    }).then(function (html) {
      var source = new DOMParser().parseFromString(html, 'text/html');
      // Match app.js's deterministic title-derived IDs for future News items
      // that become Latest News links before an editor supplies an explicit ID.
      source.querySelectorAll('.news-grid > .story').forEach(function (item) {
        if (item.id) return;
        var sourceTitle = item.querySelector('h3');
        if (!sourceTitle) return;
        var title = sourceTitle.textContent.trim();
        var hash = 2166136261;
        for (var i = 0; i < title.length; i++) hash = Math.imul(hash ^ title.charCodeAt(i), 16777619);
        item.id = 'news-' + (hash >>> 0).toString(16);
      });
      var story = source.getElementById(storyId);
      if (!story || !story.matches('.news-grid > .story')) throw new Error('The selected story could not be found.');
      renderStory(story);
    }).catch(function (error) {
      showError(error.message || 'The story could not be loaded. Please try again.');
    });
  }

  function showError(message) {
    heading.textContent = 'Story unavailable';
    status.textContent = message;
    status.hidden = false;
    retry.hidden = false;
    article.setAttribute('aria-busy', 'false');
  }

  retry.addEventListener('click', loadStory);
  loadStory();
})();
