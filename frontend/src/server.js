export const get_available_albums = async () => {
  const response = await fetch('/albums/');
  const { available_albums } = await response.json();
  return available_albums;
}

export const get_album_info = async album_name => {
  const response = await fetch('/albums/' + album_name);
  const data = await response.json();
  return data;
}

export const capture_image_to_album = async album_name => {
  const response = await fetch('/albums/' + album_name, { method: 'POST'})
  const data = await response.json();
  return data;
}

export const create_or_update_album = async (album_name, description) => {
  const request_body = { "album_name": album_name }
  if (description) {
    request_body["description"] = description
  }

  const response = await fetch('/albums/', {
    method: 'POST',
    body: JSON.stringify(request_body),
    headers: {
      'Content-Type': 'application/json',
      'Accept': 'application/json',
    },
  })
  const data = await response.json();
  return data;
}
