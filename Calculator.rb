require "./Validator.rb"
class Calculator
  include Validator
  attr_accessor :number_1, :number_2, :type
  INPUT_TYPES = { '1' => 'add', '2' => 'subtract', '3' => 'multiply', '4' => 'divide' }

  def initialize(number_1, number_2, type)
    @number_1 = number_1
    @number_2 = number_2    
    @type = type
  end

  def self.start
    puts "Choose an option"
    puts "1. Add"
    puts "2. Subtract"
    puts "3. Multiply"
    puts "4. Division"
    take_user_input.calculate

  end

  #user inputs
  def self.take_user_input
    print ("Option Number: ")
    type = gets.chomp
    print ("First Number: ")
    number_1 = gets.chomp
    print ("Second Number: ")
    number_2 = gets.chomp
    new(number_1, number_2, type)
  end

  def calculate
    if numeric
      puts send(INPUT_TYPES[type])
    else
      puts"Sorry! You have entered an invalid number.."
    end
  end
  #performing the various calculations
  
  def add
	  number_1 + number_2
  end

  def subtract
	  number_1 - number_2
  end

  def multiply
	  number_1 * number_2
  end

  def divide
	  if number_2 == 0
		  "Sorry! A number can't be divided by Zero.."
	  else	
		 number_1 / number_2
	  end
  end
 end

Calculator.start
