// author: Denson Smith
// stoa--fdf §29.1 fixture: prospector (geo project). Carries REAL Layer-S signals:
//   sdk_imports: @googlemaps/js-api-loader  (Maps-JS SDK import -> google-maps)
//   url_patterns: maps.googleapis.com       (maps tile/api URL  -> google-maps)
// (spatial-data is carried as a data_signal via the .geojson resource + signals manifest.)
import { Loader } from "@googlemaps/js-api-loader";

// a commented-out import that MUST NOT be flagged (AST/comment-aware discipline, §28):
// import { documentai } from "google.cloud.documentai";

export async function renderMap(el) {
  const loader = new Loader({ apiKey: window.MAPS_KEY });
  await loader.load();
  // outbound maps tile fetch — the url_pattern signal
  const res = await fetch("https://maps.googleapis.com/maps/api/js");
  return res.ok;
}
