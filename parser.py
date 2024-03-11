from types import NoneType
from typing import Union
from scanner import Scanner, Token, TokenType

JsonValue = Union["JsonObject", "JsonArray", bool, str, float, int, NoneType]
JsonObject = dict[str, JsonValue]
JsonArray = list[JsonValue]

class Parser:
  def __init__(self, tokens: list[Token]):
    self.tokens = tokens
    self.current = 0
    
  def parse(self) -> JsonValue:
    token = self.advance()
    return self.parse_token(token)
    
  def parse_token(self, token: Token):
    match token.tokenType:
      case TokenType.LEFT_BRACE:
        return self.parse_object()
      case TokenType.LEFT_BRACKET:
        return self.parse_array()
      case TokenType.STRING | TokenType.NUMBER | TokenType.BOOL | TokenType.NULL:
        return token.value
      case _:
        raise ValueError(f"Unexpected token: {token.tokenType}")
        
  def parse_object(self) -> JsonObject:
    obj = {}
    key_token = self.advance()
    # print(key_token.tokenType)
    while key_token.tokenType != TokenType.RIGHT_BRACE:
      self.check_key_token_err(token = key_token)
        
      self.consume(TokenType.COLON)  
      
      value_token = self.advance()

      obj[key_token.value] = self.parse_token(value_token)

      self.consume_comma_unless(TokenType.RIGHT_BRACE)

      key_token = self.advance()
    return obj  
      
  def parse_array(self) -> JsonArray:
    res = []
    token = self.advance()
    while token.tokenType != TokenType.RIGHT_BRACKET:
      if token.tokenType == TokenType.EOF:
        raise ValueError("Invalid array")
  
      res.append(self.parse_token(token))   

      self.consume_comma_unless(TokenType.RIGHT_BRACKET)

      token = self.advance()
      
    return res
  
  def advance(self):
    res = self.tokens[self.current]
    self.current += 1
    return res
    
  def consume(self, tokenType: TokenType):
    if self.current_token().tokenType != tokenType:
      raise ValueError(f"Unexpected token type")
    self.current += 1  
    
  def consume_comma_unless(self, exception: TokenType):
    if self.current_token().tokenType == TokenType.COMMA:
        self.advance()
        return

    if self.current_token().tokenType != exception:
        raise ValueError("Missing comma unless followed by", str(exception))

  def current_token(self) -> Token:
    return self.tokens[self.current]

  def check_key_token_err(self, token: Token):
    if token.tokenType == TokenType.EOF:
      raise ValueError("Unterminated object")
    elif token.tokenType != TokenType.STRING:
      raise ValueError("Object key must be a string")
