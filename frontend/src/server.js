export const get_available_album_data = async () => {
  const response = await fetch('/albums/');
  const data = await response.json();
  return data;
}

export const get_album_info = async album_name => {
  const response = await fetch('/albums/' + album_name);
  const data = await response.json();
  return data;
}

export const get_last_image_url = async album_name => {
  const response = await fetch('/albums/' + album_name + "/last_image");
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

export const get_qr_codes = async () => {
  const response = await fetch('/qr_codes/');
  const data = await response.json();
  return data;
}
