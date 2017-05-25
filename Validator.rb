module Validator
	def numeric
  	true if ((@number_1=Float(@number_1)) && (@number_2 = Float(@number_2)))  rescue false
	end
end