# Merge sort
def MergeSort(l, N=1, asc_list=[1]):
    """
    Perform merge sort on the list of statements

    Parameters:
        l (list): list of tuples to be sorted
        N (int): length of each tuple
        asc_list (list): list of integers indicating the order of sorting for each tuple element

    Returns:
        l (list): sorted list of tuples
    """
    # Make sure each tuple has the same length (N)
    for i in range(len(l)):
        while len(l[i]) != N:
            raise ValueError("Each tuple must have the same length but received", l[i], "with length", len(l[i]), "when N is", N, "and the previous length is", len(l[i-1]))
    
    # Make sure the length of asc_list is the same as the length of each tuple
    if len(asc_list) != N:
        raise ValueError("The length of asc_list must be the same as the length of each tuple")
    
    # Make sure each element in asc_list is either 1 or 0
    for i in range(len(asc_list)):
        if asc_list[i] not in [0, 1]:
            raise ValueError("Each element in asc_list must be either 1 or 0")
    

    if len(l)>1:
        mid = int(len(l)/2)
        # Split the list into two halves
        leftHalf = l[:mid]
        rightHalf = l[mid:]

        leftHalf = MergeSort(leftHalf, N, asc_list)
        rightHalf = MergeSort(rightHalf, N, asc_list)

        leftIndex, rightIndex, mergeIndex = 0, 0, 0

        mergeList = l
        while leftIndex < len(leftHalf) and rightIndex < len(rightHalf):

            # If tuples are equal, choose the left one
            if leftHalf[leftIndex] == rightHalf[rightIndex]:
                mergeList[mergeIndex] = leftHalf[leftIndex]
                leftIndex += 1
                mergeIndex += 1
                continue
            
            # Otherwise, compare the tuples based on the order specified in asc_list
            left_key = leftHalf[leftIndex] 
            right_key = rightHalf[rightIndex]

            for i in range(N):
                # For ascending order
                if asc_list[i] == 1:
                    if left_key[i] < right_key[i]:
                        mergeList[mergeIndex] = leftHalf[leftIndex]
                        leftIndex += 1
                        break
                    elif left_key[i] > right_key[i]:
                        mergeList[mergeIndex] = rightHalf[rightIndex]
                        rightIndex += 1
                        break
                    # Elements are equal, continue to compare the next element in the tuple
                    else:
                        continue

                # For descending order
                else:
                    if left_key[i] > right_key[i]:
                        mergeList[mergeIndex] = leftHalf[leftIndex]
                        leftIndex += 1
                        break
                    elif left_key[i] < right_key[i]:
                        mergeList[mergeIndex] = rightHalf[rightIndex]
                        rightIndex += 1
                        break
                    # Elements are equal, continue to compare the next element in the tuple
                    else:
                        continue

            mergeIndex += 1

        # Handle those items still left in the left Half 
        while leftIndex < len(leftHalf):
            mergeList[mergeIndex] = leftHalf[leftIndex]
            leftIndex+=1
            mergeIndex+=1

        # Handle those items still left in the right Half 
        while rightIndex < len(rightHalf):
            mergeList[mergeIndex] = rightHalf[rightIndex]
            rightIndex+=1
            mergeIndex+=1

        return mergeList
    
    return l