#include <stdio.h>
#include <iostream>
#include <vector>
#include <string>
#include <locale> 
#include <cstdlib> 
#include <clocale> 
#include <map>

#pragma once

typedef std::string token_type;

class Token {

public:
    std::string token; 
    // constructor
    Token() : token("") {}
    
    Token(const std::string& str) : token(str) {}

    // method to add character to token
    void push_back(char c) {
        token.push_back(c);
    }
    // method to add character to add std::string 
    void push_back(const std::string& str) {
        token += str;
    }
    // method to access the internal string
    const std::string& get_token() const {
        return token;
    }
    // token size
    int size() const { return token.size(); }

    // access index of token non const
    char& operator[](int index) {
        return token[index];
    }

    // access index of token const
    const char& operator[](int index) const {
        return token[index];
    }

    void clear() { token.clear(); }
 
    bool is_stopword() const {
        // change to a hash!!
        std::vector<std::string> stopwords = {"para"};
        for (int i = 0; i < stopwords.size();i++){
            if (stopwords[i] == token) return true;
        }
        return false;
    }

    Token to_lower(Token& word) {
        for (int i = 0; i < word.size(); i++) {
            if (65 <= word[i] && word[i] <= 90) {
                word[i] = word[i] + 32;  
            }
        return word;
    }
    }
};

class Document {
    public: 
    std::vector<Token> document;

    // constructor
    Document() : document({}) {}
    
    Document(const std::vector<Token>& vec) : document(vec) {}

    // method to add character to token
    void push_back(Token t) {
        document.push_back(t);
    }
    
    // method to access the internal string
    const std::vector<Token>& get_document() const {
        return document;
    }
    // token size
    int size() const { return document.size(); }

    // access index of token non const
    Token operator[](int index) {
        return document[index];
    }

    // access index of token const
    const Token& operator[](int index) const {
        return document[index];
    }


    bool is_alpha(char c) {
        if (65 <= c && c <= 90) {
            return true;
        } else if (97 <= c && c <= 122) {
            return true;
        } else {
            return false;
        }
    }

    bool is_space(char c) {
        if (c == 32) {
            return true;
        } else {
            return false;
        }
    }


    std::string to_lower(std::string& word) {
        for (int i = 0; i < word.size(); i++) {
            if (65 <= word[i] && word[i] <= 90) {
                word[i] = word[i] + 32;  
            }
        }

        return word;
    }

    Document tokenize(std::string& text) {
        int i = 0;
        int n = text.length();
        Document tokens;
        Token curr;

        while (i < n) {
            if (is_alpha(text[i])) {
                curr.push_back(text[i]);
            } else if (is_space(text[i])) {
                if (curr.size() > 0) {
                    tokens.push_back(curr);
                    curr.clear();  
                }
            }
            i++;
        }

        if (curr.size() > 0) {
            tokens.push_back(curr);
        }

        return tokens;
    }


    Document remove_stopwords() const {
        Document tokens_new;
        for (int  i= 0 ; i < document.size(); i++){
        if (!document[i].is_stopword()){
            tokens_new.push_back(document[i]);
        }
        }

        return tokens_new;
    }
};

/* Pre-processing functions*/

bool is_special(wchar_t c){
    /* check for special characters*/
    return false;
}

char wchar_to_char(wchar_t wt) {
    // Setting the locale for the conversion
    std::setlocale(LC_ALL, "");

    // buffer 
    char buffer[MB_CUR_MAX]; 

    // convert the wchar_t to a multibyte character
    int bytes_written = wctomb(buffer, wt);

    // if conversion is successful, return the first character in the buffer
    if (bytes_written > 0) {
        return buffer[0];
    } else { // error
        std::cerr << "Conversion error!" << std::endl;
        return '\0';
    }
}

std::string transform_special(std::wstring &stream){
    std::string res;
    for (int i=0 ; i < stream.size() ; i++){
        if(is_special(stream[i])){
            /* Check to see if character is SP*/
        } else {
            res += wchar_to_char(stream[i]);
        }
    }
    return res;
}


