def returnIChimoku(data, spanPeriod=52, conversion_line_period=9, baseline_period=26):
    reMergeData = reMerge(data)
    spanA = np.array([])
    spanB = np.array([])
    conversion_Line = np.array([])
    base_line = np.array([])
    for i, v in enumerate(reMergeData.items()):
        ichimoku = reMergeData[FILE.SYMBOL[i]].ta.ichimoku(include_chikou=False, tenkan=conversion_line_period,
                                                           kijun=baseline_period,
                                                           senkou=spanPeriod)
        currentIchimoku = ichimoku[0]
        ichi_col = currentIchimoku.columns.values
        spanA = np.append(spanA, currentIchimoku[ichi_col[0]].to_numpy())
        spanB = np.append(spanB, currentIchimoku[ichi_col[1]].to_numpy())
        conversion_Line = np.append(conversion_Line, currentIchimoku[ichi_col[2]].to_numpy())
        base_line = np.append(base_line, currentIchimoku[ichi_col[3]].to_numpy())

        constant = int(len(spanA) / len(FILE.SYMBOL))

        spanA = spanA.reshape(constant, len(FILE.SYMBOL))
        spanB = spanB.reshape(constant, len(FILE.SYMBOL))
        conversion_Line = conversion_Line.reshape(constant, len(FILE.SYMBOL))
        base_line = base_line.reshape(constant, len(FILE.SYMBOL))
    return [spanA, spanB, conversion_Line, base_line, ]
