#problem 2
#a)
class ParkingPermit(object):
    '''represents a parmking permit w owner, number of months, and fee schedule'''
    def __init__(self, name: str, numMonths: int, feeSchedule: dict) -> None:
        '''stores the name, number of months, and fee schedule in the object
        pre: name is a string, numMonths is a non-negative integer, feeSchedule is a dictionary with non-negative ints
        post: stores the name, number of months, and fee schedule in the object'''
        self.name = name
        self.numMonths = numMonths
        self.feeSchedule = feeSchedule

    def __str__(self) -> str: 
        '''returns a string representation of the object
        pre: name is a string, numMonths is a non-negative integer, feeSchedule is a dictionary with non-negative ints
        post: returns a string representation of the object'''
        return "Owner: {}, Number of Months: {}," \
        " Fee Schedule: {}".format(self.name, self.numMonths, self.feeSchedule)

    def __repr__(self) -> str:
        '''returns a string representation of the object'''
        return self.__str__()

    def cost(self) -> float:
        '''returns the cost of the permit based on the fee schedule and number of months
        pre: subclass implements cost method
        post: returns the cost of the permit based on the fee schedule and number of months'''
        pass #using pass as placeholder bc tye actual implementation will be in the subclasses whihc provide their respective cost methods
#b)
class StudentPermit(ParkingPermit):
    ''''represents a student parking permit with owner, number of months, fee schedule, and number vehicles'''
    def __init__(self, name: str, numMonths: int, feeSchedule: dict, regVehicles: int) -> None:
        ''''stores the name, months, fee schedule, and number of vehicles in the object'''
        ParkingPermit.__init__(self, name, numMonths, feeSchedule)
        self.regVehicles = regVehicles

    def __str__(self) -> str:
        '''returns a string representation of the object'''
        return "Owner: {}, Number of Months: {}, Fee Schedule: {}," \
        " Registered Vehicles: {}, Cost: ${}".format(self.name, self.numMonths,
                                          self.feeSchedule, self.regVehicles, self.cost())

    def __repr__(self) -> str:
        '''returns a string representation of the object'''
        return self.__str__()
#c)
    def cost(self) -> float:
        '''returns the total cost of the student permit
        pre: feeSchedule is a dictionary with non-negative ints, numMonths is a non-negative integer, regVehicles is a non-negative integer
        post: returns the total cost of the student permit'''
        total = self.feeSchedule["student"] * self.numMonths 
        if (self.regVehicles) > 1:
            total += (self.regVehicles - 1) * self.feeSchedule["vehicle"]
        return total 

class FacultyPermit(ParkingPermit):  
    '''represents a faculty parking permit with owner, number of months, fee schedule, and garage access'''
    def __init__(self, name: str, numMonths: int, feeSchedule: dict, garAccess: bool) -> None:
        '''stores the name, months, fee schedule, and garage access in the object'''
        ParkingPermit.__init__(self, name, numMonths, feeSchedule)
        self.garAccess = garAccess
#d)
    def __str__(self) -> str:
        '''returns a string representation of the object'''
        return "Owner: {}, Number of Months: {}, Fee Schedule: {}," \
        " Garage Access: {}, Cost: ${}".format(self.name, self.numMonths,
                                          self.feeSchedule, self.garAccess, self.cost())

    def __repr__(self) -> str:
        '''returns a string representation of the object'''
        return self.__str__()

    def cost(self) -> float:
        '''returns the total cost of the faculty permit
        pre: feeSchedule is a dictionary with non-negative ints, numMonths is a non-negative integer, garAccess is a bool
        post: returns the total cost of the faculty permit'''
        total = self.feeSchedule["faculty"] * self.numMonths
        if self.garAccess == True:
            total += self.feeSchedule["garage"] * self.numMonths
        return total
#e)
def summarize_list(permits: list) -> float:
    '''prints the string representation of each permit in the list and returns the total revenue from all permits
    pre: permits is a list of ParkingPermits
    post: prints the string representation of each permit in the list and returns the total revenue from all permits'''
    print("All permit information and total revenue:")
    revenue = 0.00
    for permit in permits:
        print(permit.__str__())
        revenue += permit.cost()
    return revenue
#f)
def main():
    #fee schedule dictionary
 
    fee_schedule = {
        "student" : 25,
        "faculty" : 40,
        "vehicle" : 10,
        "garage" : 15
    }

    #creating a list of objects (my mixed permits) 
    parkingPermits = [
        StudentPermit("Tim Don", 12, fee_schedule, 1),
        StudentPermit("Lucy Lu", 8, fee_schedule, 2),
        StudentPermit("Da Boss", 20, fee_schedule, 4),
        FacultyPermit("Kim Pet", 6, fee_schedule, True),
        FacultyPermit("Fred Wane", 11, fee_schedule, False),
        FacultyPermit("Parker Lamb", 4, fee_schedule, True)
        ]

    #calling summarize_list and storing the returned total in output
    output = summarize_list(parkingPermits)
    print ("Total Revenue: ${:.2f}".format(output)) #printing the revenue two to decimal places
    print('Jorn Rutkis')
    print('Z-Number: Z23737550')
if __name__ == "__main__":
    main()