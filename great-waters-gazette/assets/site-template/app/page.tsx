const weather = [
  ['Wed 09', 'Partly cloudy (1%)', '91 / 72'],
  ['Thu 10', 'Partly cloudy (23%)', '91 / 73'],
  ['Fri 11', 'Scattered storms (58%)', '90 / 72'],
  ['Sat 12', 'Scattered storms (44%)', '88 / 72'],
  ['Sun 13', 'Partly cloudy (24%)', '91 / 71'],
];

const stories = [
  ['AI Story of the Day', 'AI labs are asking governments and rivals for shared restraints as capabilities accelerate.', 'https://www.axios.com/2026/09/09/openai-artificial-general-intelligence-safety'],
  ['Microsoft 365 Copilot', 'Copilot can ground answers in authorized private Viva Engage posts; tip: ask for expert consensus.', 'https://learn.microsoft.com/en-us/microsoft-365/copilot/release-notes'],
  ['ChatGPT', 'ChatGPT Images 2.5 improves editing and speed; tip: sketch a layout before generating the image.', 'https://openai.com/index/introducing-chatgpt-images-2-5/'],
  ['Tesla Manufacturing & Expansion', "Samsung's Taylor 2nm fab is reportedly booked by Tesla AI5 and AI6 chip orders.", 'https://www.trendforce.com/news/2026/09/09/news-samsung-taylor-fab-reportedly-fully-booked-for-2nm-before-operations-begin-fab-2-preparations-accelerate/'],
  ['Lighting Industry - Story One', "PTAB invalidated every challenged claim in Feit Electric's white-filament LED patent.", 'https://edisonreport.com/2026/09/08/ptab-finds-all-challenged-claims-in-feit-electric-led-patent-unpatentable/'],
  ['Lighting Industry - Story Two', 'Orion won a second multimillion-dollar hyperscaler order for data-center LED lighting.', 'https://edisonreport.com/2026/09/08/orion-secures-second-multimillion-dollar-data-center-order-from-global-hyperscaler/'],
  ['3D Printing News', "California's AB 2047 printer-control bill passed the legislature and awaits the governor.", 'https://www.fabbaloo.com/news/california-ab-2047-3d-printer-bill-passes-legislature-awaits-governors-decision'],
  ['Porsche 997 & 911', 'Owners compare a 997.1 Carrera 4 and Carrera S on traction, steering feel and buying risk.', 'https://www.reddit.com/r/porsche911/comments/1vw7eqp/9971_carrera_4_vs_carrera_s/'],
  ['AI-Powered Solopreneur Business', 'Opportunity: sell same-day catalog-image refreshes to small retailers with Images 2.5.', 'https://openai.com/index/introducing-chatgpt-images-2-5/'],
  ['Anna Maria Island News', "About 150 residents joined Anna Maria's town hall on the city's evolving parking study.", 'https://amisun.com/anna-maria-hosts-parking-study-meeting/'],
  ['Lake Oconee News', 'A Fiber Arts Gathering brings local makers together in Madison today.', 'https://lakeoconeelife.com/lake-oconee-calendar-of-events'],
];

export default function Home() {
  return (
    <main className="gazette-shell">
      <article className="gazette" aria-labelledby="gazette-title">
        <header className="masthead">
          <img className="brand-mark" src="/app-icon-192.png" alt="Great Waters Gazette golf course and lake mark" />
          <p className="edition-label">The morning edition</p>
          <h1 id="gazette-title">Great Waters Gazette</h1>
          <p className="edition-date">Wednesday, September 9, 2026</p>
        </header>

        <section className="lead-grid" aria-label="Weather and featured photograph">
          <div className="weather-panel">
            <h2>ZIP 31024 - 5-Day Forecast</h2>
            <div className="weather-list">
              {weather.map(([day, condition, temperatures]) => (
                <div className="weather-row" key={day}>
                  <strong>{day}</strong><span>{condition}</span><span>{temperatures}</span>
                </div>
              ))}
            </div>
            <a className="source-link" href="https://weather.com/us/georgia/eatonton/postcode/31024/tenday">Weather Channel - 11:16 AM EDT</a>
          </div>

          <figure className="featured-photo">
            <a href="https://commons.wikimedia.org/wiki/File:Sunset_over_Trommekilen_from_Norrkila_6.jpg">
              <img src="/featured-photo.jpg" alt="Sunset over Trommekilen and Brofjorden in Lysekil, Sweden" />
            </a>
            <figcaption><strong>Yesterday&apos;s Picture:</strong> Sunset over Trommekilen and Brofjorden in Lysekil, Sweden.{' '}<a href="https://commons.wikimedia.org/wiki/File:Sunset_over_Trommekilen_from_Norrkila_6.jpg">W.carter / Wikimedia Commons / CC0</a></figcaption>
          </figure>
        </section>

        <aside className="stoic-card">
          <h2>Today&apos;s Stoic Practice</h2>
          <p>Meet the next duty without rehearsing its difficulty; attention belongs to the action in front of you. <a href="https://dailystoic.com/podcast/">Daily Stoic</a></p>
        </aside>

        <section className="news-list" aria-label="Today's news">
          {stories.map(([section, summary, url]) => (
            <article className="news-item" key={section}>
              <h2>{section}</h2>
              <p><span>{summary}</span>{' '}<a href={url}>Read more</a></p>
            </article>
          ))}
        </section>

        <footer>A concise morning digest - sources linked in every section</footer>
      </article>
    </main>
  );
}
