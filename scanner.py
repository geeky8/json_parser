from enum import Enum, auto
from typing import Any

class TokenType(Enum):
  STRING = auto()
  NUMBER = auto()
  BOOL = auto()
  NULL = auto()

  LEFT_BRACE = auto()
  RIGHT_BRACE = auto()
  LEFT_BRACKET = auto()
  RIGHT_BRACKET = auto()
  COMMA = auto()
  COLON = auto()
  EOF = auto()

class Token:
  def __init__(self, tokenType : TokenType, value: Any):
    self.tokenType = tokenType
    self.value = value
  def printMe(self):
    print(self.tokenType, self.value)  

class Scanner:
  # intitalize the list of token with appropriate Custom-Object
  tokens : list[Token]
  def __init__(self, text: str):
    self.source = text
    self.start = 0
    self.current = 0
    self.line = 1
    self.tokens = []

  def scan(self) -> list[Token]:
    while not self.is_at_end():
        self.start = self.current
        self.scan_token()

    self.tokens.append(Token(TokenType.EOF, None))
    return self.tokens

  def is_at_end(self)-> bool:
    return self.current >= len(self.source)

  def scan_token(self):
    ch = self.advance()
    match ch:
      case '{':
        self.tokens.append(Token(TokenType.LEFT_BRACE, None))  
      case '}':
        self.tokens.append(Token(TokenType.RIGHT_BRACE, None))
      case '[':
        self.tokens.append(Token(TokenType.LEFT_BRACKET, None))
      case ']':
        self.tokens.append(Token(TokenType.RIGHT_BRACKET, None))
      case ':':
        self.tokens.append(Token(TokenType.COLON, None))
      case ',':
        self.tokens.append(Token(TokenType.COMMA, None))
      case '"': 
        self.add_string()  
      case '\n':
        self.line += 1
      case ' ':
        pass
      case '-':
        if self.current_char().isdigit():
          self.add_number()
        else:
          raise ValueError("- should be followed by a number")
      case _:
        if ch.isdigit(): self.add_number()
        elif ch.isalpha(): self.add_keyword()
        else: raise ValueError(f"Unexpected character: {ch}")

  # check for int and float types
  def add_number(self):
    while self.current_char().isdigit():
      self.advance()
    if self.current_char() == '.':
      if not self.next_char.isdigit():
        raise ValueError("Invalid number")
      while self.current_char().isdigit():
        self.advance()

      
    self.tokens.append(Token(TokenType.NUMBER, float(self.source[self.start:self.current])))
        
  def add_keyword(self):
    while self.current_char().isalpha():
      self.advance()
      
    key = self.source[self.start:self.current]
    
    match key:
      case "true": self.tokens.append(Token(TokenType.BOOL, True))
      case "false": self.tokens.append(Token(TokenType.BOOL, False))
      case _: raise ValueError(f"Unexpected keyword: {key}")
        
    
  def add_string(self):
    while self.current_char().isalpha() and not self.is_at_end():
      self.advance()
    if self.is_at_end():
      raise ValueError("Unterminated string")
    # before consumeing any other new character we have to update the place of self.current
    self.advance()  
    self.tokens.append(Token(TokenType.STRING,self.source[self.start+1: self.current-1]))
    
  def advance(self) -> str:
    if not self.is_at_end ():
      ch = self.source[self.current]
      self.current += 1
      return ch
    else: return ""
      
  def current_char(self) -> str:
    if self.is_at_end():
      return ""
    return self.source[self.current]  

  def next_char(self) -> str:
    if self.current+1 >= len(self.source):
      return ""
    return self.source[self.current+1]  
    
    
          
          

    
    
