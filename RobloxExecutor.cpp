#include <iostream>
#include <string>
#include <curl/curl.h>
#include <jsoncpp/json/json.h>

class RobloxExecutor {
private:
    std::string securityToken;
    std::string placeId;
    std::string xsrfToken;

    static size_t WriteCallback(void* contents, size_t size, size_t nmemb, std::string* userp) {
        size_t totalSize = size * nmemb;
        userp->append((char*)contents, totalSize);
        return totalSize;
    }

    std::string getCookieValue(const std::string& cookies, const std::string& cookieName) {
        size_t pos = cookies.find(cookieName + "=");
        if (pos == std::string::npos) return "";
        
        pos += cookieName.length() + 1;
        size_t endPos = cookies.find(";", pos);
        if (endPos == std::string::npos) endPos = cookies.length();
        
        return cookies.substr(pos, endPos - pos);
    }

    std::string getXsrfToken() {
        CURL* curl;
        CURLcode res;
        std::string readBuffer;
        std::string cookies;

        curl = curl_easy_init();
        if(curl) {
            struct curl_slist *headers = NULL;
            headers = curl_slist_append(headers, ("Cookie: .ROBLOSECURITY=" + securityToken).c_str());
            
            curl_easy_setopt(curl, CURLOPT_URL, "https://www.roblox.com/home");
            curl_easy_setopt(curl, CURLOPT_HTTPHEADER, headers);
            curl_easy_setopt(curl, CURLOPT_FOLLOWLOCATION, 1L);
            curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, WriteCallback);
            curl_easy_setopt(curl, CURLOPT_WRITEDATA, &readBuffer);
            curl_easy_setopt(curl, CURLOPT_HEADERDATA, &cookies);
            
            res = curl_easy_perform(curl);
            curl_slist_free_all(headers);
            curl_easy_cleanup(curl);
            
            if(res == CURLE_OK) {
                size_t pos = readBuffer.find("XsrfToken\":\"");
                if (pos != std::string::npos) {
                    pos += 12; // Length of "XsrfToken\":\""
                    size_t endPos = readBuffer.find("\"", pos);
                    if (endPos != std::string::npos) {
                        return readBuffer.substr(pos, endPos - pos);
                    }
                }
            }
        }
        return "";
    }

public:
    bool authenticate(const std::string& cookie, const std::string& pId) {
        securityToken = cookie;
        placeId = pId;
        xsrfToken = getXsrfToken();
        return !xsrfToken.empty();
    }

    bool executeScript(const std::string& script) {
        if (xsrfToken.empty()) {
            std::cout << "Error: Not authenticated" << std::endl;
            return false;
        }

        CURL* curl;
        CURLcode res;
        std::string readBuffer;

        curl = curl_easy_init();
        if(curl) {
            struct curl_slist *headers = NULL;
            headers = curl_slist_append(headers, ("Content-Type: application/json"));
            headers = curl_slist_append(headers, ("X-CSRF-TOKEN: " + xsrfToken).c_str());
            headers = curl_slist_append(headers, ("Cookie: .ROBLOSECURITY=" + securityToken).c_str());
            
            Json::Value jsonData;
            jsonData["script"] = script;
            
            Json::StreamWriterBuilder builder;
            std::string jsonString = Json::writeString(builder, jsonData);
            
            curl_easy_setopt(curl, CURLOPT_URL, ("https://www.roblox.com/v1/scripts?placeId=" + placeId).c_str());
            curl_easy_setopt(curl, CURLOPT_HTTPHEADER, headers);
            curl_easy_setopt(curl, CURLOPT_POST, 1L);
            curl_easy_setopt(curl, CURLOPT_POSTFIELDS, jsonString.c_str());
            curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, WriteCallback);
            curl_easy_setopt(curl, CURLOPT_WRITEDATA, &readBuffer);
            
            res = curl_easy_perform(curl);
            curl_slist_free_all(headers);
            curl_easy_cleanup(curl);
            
            if(res == CURLE_OK) {
                std::cout << "Script executed successfully: " << readBuffer << std::endl;
                return true;
            } else {
                std::cout << "Error executing script: " << curl_easy_strerror(res) << std::endl;
                return false;
            }
        }
        return false;
    }
};

extern "C" {
    RobloxExecutor* create_executor() {
        return new RobloxExecutor();
    }
    
    void destroy_executor(RobloxExecutor* executor) {
        delete executor;
    }
    
    bool authenticate_executor(RobloxExecutor* executor, const char* cookie, const char* placeId) {
        return executor->authenticate(std::string(cookie), std::string(placeId));
    }
    
    bool execute_script(RobloxExecutor* executor, const char* script) {
        return executor->executeScript(std::string(script));
    }
}