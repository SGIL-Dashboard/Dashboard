import axios from "axios";
import CryptoJS from "crypto-js";
import toast from "react-hot-toast";
import FormData from "form-data";

const encrypt = (text, key = "salt") =>
  CryptoJS.AES.encrypt(text, key).toString();
const decrypt = (cipherText, key = "salt") =>
  CryptoJS.AES.decrypt(cipherText, key).toString(CryptoJS.enc.Utf8);
export const insertCommas = (number) => {
  // let initialText = `${number}`.slice(0 , -3);
  // const lastThree = `${number}`.slice(-3);
  return number.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
  // return`${initialText},${lastThree}`;
};
export const makeApiRequest = async ({
  method,
  urlPath,
  body,
  encryptedKeys,
  convertToFormData,
  token,
}) => {
  let config = {};
  const baseApiUrl = "http://api.sgillabs.com/";
  config.method = method;
  config.url = `${baseApiUrl}${urlPath}`;
  if (token) {
    config.headers = { Authorization: `Bearer ${token}` };
  }
  if (convertToFormData && body) {
    config.headers = {
      ...config.headers,
      "Content-Type": "multipart/form-data",
    };
    Object.entries(body).map(([ids, val]) => {
      if (typeof val === "string") {
        if (encryptedKeys && encryptedKeys?.includes(ids)) {
          body[ids] = encrypt(val);
        }
      } else if (!(val instanceof Blob)) {
        body[ids] = JSON.stringify(val);
      }
    });
  } else if (encryptedKeys && body) {
    encryptedKeys.map((val) => {
      if (typeof body[val] === "string") {
        body[val] = encrypt(body[val]);
      }
    });
  }
  if (method === "get") {
    config.params = body;
  } else {
    config.data = body;
  }
  let data, error;
  try {
    data = await axios(config);
  } catch (err) {
    error = err;
  }
  return { error, data };
};
export const handleFileCheck = (file) => {
  const allowedFileExtensions = ["xlsx"];

  const splittedArray = file.name.split(".");

  const result = allowedFileExtensions.includes(
    splittedArray[splittedArray.length - 1].toLowerCase()
  );
  if (!result) {
    toast.error("File type should be xlsx format");
  }
  return result;
};
export const generateUniqueId = () => {
  return new Date().getTime() + "" + Math.floor(Math.random() * 10000000);
};
export const getUniqueId = () => {
  try {
    const uniqueId = localStorage.getItem("auth");
    return decrypt(uniqueId);
  } catch {
    const uniqueId = generateUniqueId();
    localStorage.setItem("auth", encrypt(uniqueId));
    return uniqueId;
  }
};
